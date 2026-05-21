from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.conf import settings

from django.contrib.auth import get_user_model

from .forms import RegisterForm

from .models import EmailOTP, User

from providers.models import ProviderApplication

from bookings.models import Booking

import resend
resend.api_key = settings.RESEND_API_KEY

# =========================
# ✅ REGISTER
# =========================
def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(

            request.POST,

            request.FILES
        )

        if form.is_valid():

            try:

                # =========================
                # 🔥 CREATE USER
                # =========================
                user = form.save(commit=False)

                # 🔥 SAVE NAME
                user.first_name = form.cleaned_data.get(
                    'first_name'
                )

                # 🔥 SAVE PHONE
                user.phone = form.cleaned_data.get(
                    'phone'
                )

                # 🔥 EMAIL VERIFICATION REQUIRED
                user.is_active = False

                user.is_email_verified = False

                user.save()

                # =========================
                # 🔥 PROVIDER APPLICATION
                # =========================
                if user.role == 'provider':

                    application = ProviderApplication.objects.create(

                        user=user,

                        aadhar_card=request.FILES.get(
                            'aadhar_card'
                        ),

                        passport_photo=request.FILES.get(
                            'passport_photo'
                        ),

                        cv=request.FILES.get(
                            'cv'
                        ),

                        driving_license=request.FILES.get(
                            'driving_license'
                        ),
                    )

                    services = form.cleaned_data.get(
                        'services'
                    )

                    if services:

                        application.services.set(
                            services
                        )

                # =========================
                # 🔥 CREATE OTP
                # =========================
                otp_obj = EmailOTP.objects.create(
                    user=user
                )

                otp_obj.generate_otp()

                # =========================
                # 🔥 SEND OTP USING RESEND
                # =========================
                try:

                    resend.Emails.send({

                        "from": "onboarding@resend.dev",

                        "to": user.email,

                        "subject": "Email Verification OTP",

                        "html": f"""

                            <div style="font-family: Arial; padding: 20px;">

                                <h2 style="color:#000;">
                                    Email Verification
                                </h2>

                                <p>
                                    Hello {user.first_name},
                                </p>

                                <p>
                                    Your OTP verification code is:
                                </p>

                                <h1 style="letter-spacing: 5px; color:#000;">
                                    {otp_obj.otp}
                                </h1>

                                <p>
                                    Do not share this OTP with anyone.
                                </p>

                                <br>

                                <p>
                                    Service Platform Team
                                </p>

                            </div>

                        """
                    })

                    messages.success(

                        request,

                        "📧 OTP sent successfully to your email."
                    )

                except Exception as resend_error:

                    print(
                        "RESEND ERROR:",
                        resend_error
                    )

                    messages.warning(

                        request,

                        f"⚠️ Email failed but your OTP is: {otp_obj.otp}"
                    )

                # =========================
                # 🔥 REDIRECT TO VERIFY PAGE
                # =========================
                return redirect(

                    'verify_email',

                    user_id=user.id
                )

            except Exception as e:

                print(
                    "REGISTER ERROR:",
                    e
                )

                messages.error(

                    request,

                    "❌ Registration failed. Please try again."
                )

                return redirect(
                    'register'
                )

        else:

            print(form.errors)

            messages.error(

                request,

                "⚠️ Please correct the errors below."
            )

    else:

        form = RegisterForm()

    return render(

        request,

        'users/register.html',

        {
            'form': form
        }
    )


# =========================
# ✅ VERIFY EMAIL
# =========================
def verify_email(request, user_id):

    User = get_user_model()

    user = get_object_or_404(
        User,
        id=user_id
    )

    otp_obj = EmailOTP.objects.filter(
        user=user
    ).last()

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        if otp_obj and otp_obj.otp == entered_otp:

            # 🔥 ACTIVATE USER
            user.is_active = True

            user.is_email_verified = True

            user.save()

            messages.success(

                request,

                "✅ Email verified successfully!"
            )

            login(
                request,
                user
            )

            # 🔥 ROLE REDIRECT
            if user.role == 'admin':

                return redirect(
                    'admin_dashboard'
                )

            elif user.role == 'provider':

                return redirect(
                    'provider_dashboard'
                )

            else:

                return redirect(
                    'home'
                )

        else:

            messages.error(

                request,

                "❌ Invalid OTP. Please try again."
            )

    return render(

        request,

        'users/verify.html',

        {
            'user': user
        }
    )


# =========================
# ✅ LOGIN
# =========================
def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password
        )

        if user:

            # =========================
            # 🚫 EMAIL VERIFICATION
            # =========================
            if not user.is_active:

                messages.warning(

                    request,

                    "📧 Please verify your email first."
                )

                return redirect(

                    'verify_email',

                    user_id=user.id
                )

            if not user.is_email_verified:

                messages.warning(

                    request,

                    "📧 Please verify your email."
                )

                return redirect(

                    'verify_email',

                    user_id=user.id
                )

            # =========================
            # 🔥 PROVIDER VALIDATION
            # =========================
            if user.role == 'provider':

                try:

                    application = ProviderApplication.objects.get(
                        user=user
                    )

                    if application.status == 'pending':

                        messages.warning(

                            request,

                            "⏳ Your provider application is under review."
                        )

                        return redirect(
                            'login'
                        )

                    elif application.status == 'rejected':

                        messages.error(

                            request,

                            "❌ Your provider application was rejected."
                        )

                        return redirect(
                            'login'
                        )

                except ProviderApplication.DoesNotExist:

                    messages.error(

                        request,

                        "⚠️ Provider application not found."
                    )

                    return redirect(
                        'register'
                    )

            # =========================
            # ✅ LOGIN USER
            # =========================
            login(
                request,
                user
            )

            messages.success(

                request,

                f"Welcome back, {user.first_name} 👋"
            )

            # =========================
            # 🔥 REDIRECT LOGIC
            # =========================
            if next_url and next_url not in ['/', 'None']:

                return redirect(next_url)

            if user.is_superuser or user.role == 'admin':

                return redirect(
                    'admin_dashboard'
                )

            elif user.role == 'provider':

                return redirect(
                    'provider_dashboard'
                )

            else:

                return redirect(
                    'home'
                )

        else:

            messages.error(

                request,

                "❌ Invalid username or password."
            )

    return render(

        request,

        'users/login.html',

        {
            'next': next_url
        }
    )


# =========================
# ✅ USER DASHBOARD
# =========================
@login_required
def user_dashboard(request):

    if request.user.role != 'customer':

        return redirect(
            'home'
        )

    bookings = Booking.objects.filter(

        user=request.user

    ).order_by('-created_at')

    return render(

        request,

        'users/dashboard.html',

        {
            'bookings': bookings
        }
    )


# =========================
# ❌ CANCEL BOOKING
# =========================
@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(

        Booking,

        id=id,

        user=request.user
    )

    if booking.status in ['completed', 'cancelled']:

        messages.warning(

            request,

            "⚠️ This booking cannot be cancelled."
        )

        return redirect(
            'user_dashboard'
        )

    booking.status = 'cancelled'

    booking.save()

    # 🔥 MAKE PROVIDER AVAILABLE AGAIN
    if booking.provider:

        booking.provider.is_available = True

        booking.provider.save()

    messages.success(

        request,

        "❌ Booking cancelled successfully!"
    )

    return redirect(
        'user_dashboard'
    )


# =========================
# ✅ LOGOUT
# =========================
def logout_view(request):

    logout(request)

    messages.info(

        request,

        "👋 Logged out successfully."
    )

    return redirect(
        'home'
    )


# =========================
# ✅ USER PROFILE
# =========================
@login_required
def profile_view(request):

    user = request.user

    if request.method == 'POST':

        # 🔥 UPDATE NAME
        user.first_name = request.POST.get(
            'first_name'
        )

        # 🔥 UPDATE PHONE
        user.phone = request.POST.get(
            'phone'
        )

        # 🔥 UPDATE PROFILE IMAGE
        if request.FILES.get('profile_image'):

            user.profile_image = request.FILES.get(
                'profile_image'
            )

        user.save()

        messages.success(

            request,

            "✅ Profile updated successfully!"
        )

        return redirect(
            'profile'
        )

    return render(
        request,
        'users/profile.html'
    )


# =========================
# ✅ FORGOT PASSWORD
# =========================
def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        # 🔥 GET USER
        user = User.objects.filter(
            email=email
        ).first()

        # ❌ EMAIL NOT FOUND
        if not user:

            messages.error(

                request,

                "❌ Email not registered."
            )

            return redirect(
                'forgot_password'
            )

        # 🔥 CREATE OTP
        otp_obj = EmailOTP.objects.create(
            user=user
        )

        otp_obj.generate_otp()

        # 🔥 SAVE SESSION
        request.session['reset_user_id'] = user.id

        # =========================
        # 🔥 SHOW RESET OTP DIRECTLY
        # =========================
        print(
            "RESET OTP:",
            otp_obj.otp
        )

        messages.success(

            request,

            f"✅ Your password reset OTP is: {otp_obj.otp}"
        )

        return redirect(
            'verify_reset_otp'
        )

    return render(

        request,

        'forgot_password.html'
    )


# =========================
# ✅ VERIFY RESET OTP
# =========================
def verify_reset_otp(request):

    user_id = request.session.get(
        'reset_user_id'
    )

    # ❌ SESSION EXPIRED
    if not user_id:

        messages.error(

            request,

            "⚠️ Session expired."
        )

        return redirect(
            'forgot_password'
        )

    # 🔥 GET USER
    user = get_object_or_404(

        User,

        id=user_id
    )

    # 🔥 GET OTP
    otp_obj = EmailOTP.objects.filter(

        user=user

    ).last()

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        # ✅ OTP MATCH
        if otp_obj and otp_obj.otp == entered_otp:

            messages.success(

                request,

                "✅ OTP verified successfully."
            )

            return redirect(
                'reset_password'
            )

        else:

            messages.error(

                request,

                "❌ Invalid OTP."
            )

    return render(

        request,

        'users/verify.html'
    )


# =========================
# ✅ RESET PASSWORD
# =========================
def reset_password(request):

    user_id = request.session.get(
        'reset_user_id'
    )

    # ❌ SESSION EXPIRED
    if not user_id:

        messages.error(

            request,

            "⚠️ Session expired."
        )

        return redirect(
            'forgot_password'
        )

    # 🔥 GET USER
    user = get_object_or_404(

        User,

        id=user_id
    )

    if request.method == 'POST':

        password1 = request.POST.get(
            'password1'
        )

        password2 = request.POST.get(
            'password2'
        )

        # ❌ PASSWORD NOT MATCH
        if password1 != password2:

            messages.error(

                request,

                "❌ Passwords do not match."
            )

            return redirect(
                'reset_password'
            )

        # ✅ UPDATE PASSWORD
        user.set_password(password1)

        user.save()

        # 🔥 CLEAR SESSION
        request.session.pop(
            'reset_user_id',
            None
        )

        messages.success(

            request,

            "✅ Password reset successful."
        )

        return redirect(
            'login'
        )

    return render(

        request,

        'reset_password.html'
    )