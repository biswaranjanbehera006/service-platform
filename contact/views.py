from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

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
        # SEND EMAIL USING BREVO API
        # =========================================
        try:

            configuration = sib_api_v3_sdk.Configuration()

            configuration.api_key['api-key'] = settings.BREVO_API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )

            email_subject = f"📩 New Contact Message - {subject}"

            html_content = f"""
            <h2>New Contact Message</h2>

            <p><strong>Name:</strong> {name}</p>

            <p><strong>Email:</strong> {email}</p>

            <p><strong>Subject:</strong> {subject}</p>

            <p><strong>Message:</strong></p>

            <p>{message}</p>

            <hr>

            <p>Sent From ServiceHub Contact Page</p>
            """

            sender = {
                "name": "ServiceHub",
                "email": settings.DEFAULT_FROM_EMAIL
            }

            to = [
                {
                    "email": settings.ADMIN_RECEIVER_EMAIL,
                    "name": "Admin"
                }
            ]

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(

                to=to,

                sender=sender,

                subject=email_subject,

                html_content=html_content
            )

            api_instance.send_transac_email(
                send_smtp_email
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