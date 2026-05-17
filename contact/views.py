from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Contact


# =====================================================
# 📩 CONTACT PAGE
# =====================================================
def contact_page(request):

    # =========================================
    # FORM SUBMIT
    # =========================================
    if request.method == 'POST':

        print("✅ CONTACT VIEW CALLED")

        # =========================================
        # GET FORM DATA
        # =========================================
        name = request.POST.get('name')

        email = request.POST.get('email')

        subject = request.POST.get('subject')

        message = request.POST.get('message')

        print(name, email, subject)

        # =========================================
        # SAVE TO DATABASE
        # =========================================
        Contact.objects.create(

            name=name,

            email=email,

            subject=subject,

            message=message
        )

        print("✅ MESSAGE SAVED TO DATABASE")

        # =========================================
        # EMAIL CONTENT
        # =========================================
        admin_subject = f"📩 New Contact Message - {subject}"

        admin_message = f"""
New Contact Message Received

----------------------------------------

Name:
{name}

Email:
{email}

Subject:
{subject}

Message:
{message}

----------------------------------------

Sent From ServiceHub Contact Page
"""

        # =========================================
        # SEND EMAIL
        # =========================================
        try:

            send_mail(

                admin_subject,

                admin_message,

                settings.EMAIL_HOST_USER,

                [settings.ADMIN_EMAIL],

                fail_silently=False
            )

            print("✅ EMAIL SENT SUCCESSFULLY")

        except Exception as e:

            print("❌ EMAIL ERROR:", e)

        # =========================================
        # SUCCESS MESSAGE
        # =========================================
        messages.success(

            request,

            "✅ Your message has been sent successfully!"
        )

        return redirect(
            'contact'
        )

    # =========================================
    # GET REQUEST
    # =========================================
    return render(

        request,

         'services/contact.html'
    )