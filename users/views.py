from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from .forms import RegisterForm
from .models import EmailOTP
from providers.models import ProviderApplication
from bookings.models import Booking


# =========================
# ✅ REGISTER
# =========================
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            # 🔥 BLOCK USER UNTIL VERIFIED
            user.is_active = False
            user.is_email_verified = False
            user.save()

            # 🔥 SAVE PROVIDER FILES
            if user.role == 'provider':
                application = ProviderApplication.objects.create(
                    user=user,
                    aadhar_card=request.FILES.get('aadhar_card'),
                    passport_photo=request.FILES.get('passport_photo'),
                    cv=request.FILES.get('cv'),
                    driving_license=request.FILES.get('driving_license'),
                )

                services = form.cleaned_data.get('services')
                if services:
                    application.services.set(services)

            # 🔥 CREATE OTP
            otp_obj = EmailOTP.objects.create(user=user)
            otp_obj.generate_otp()

            # 🔥 SEND EMAIL
            send_mail(
                "Email Verification",
                f"Your OTP is: {otp_obj.otp}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.info(request, "📧 OTP sent to your email")
            return redirect('verify_email', user_id=user.id)

        else:
            messages.error(request, "⚠️ Please fix the errors below.")

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# =========================
# ✅ VERIFY EMAIL
# =========================
def verify_email(request, user_id):

    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    otp_obj = EmailOTP.objects.filter(user=user).last()

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if otp_obj and otp_obj.otp == entered_otp:

            # 🔥 ACTIVATE USER
            user.is_active = True
            user.is_email_verified = True
            user.save()

            messages.success(request, "✅ Email verified successfully!")

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "❌ Invalid OTP")

    return render(request, 'users/verify.html', {'user': user})


# =========================
# ✅ LOGIN
# =========================
def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:

            # 🚨 HARD BLOCK (MOST IMPORTANT)
            if not user.is_active:
                messages.warning(request, "📧 Please verify your email first.")
                return redirect('verify_email', user_id=user.id)

            # 🚨 DOUBLE CHECK EMAIL
            if not user.is_email_verified:
                messages.warning(request, "📧 Please verify your email.")
                return redirect('verify_email', user_id=user.id)

            # 🔥 PROVIDER CHECK
            if user.role == 'provider':
                try:
                    application = ProviderApplication.objects.get(user=user)

                    if application.status == 'pending':
                        messages.warning(request, "⏳ Application under review.")
                        return redirect('login')

                    elif application.status == 'rejected':
                        messages.error(request, "❌ Application rejected.")
                        return redirect('login')

                except ProviderApplication.DoesNotExist:
                    messages.error(request, "⚠️ No provider application found.")
                    return redirect('register')

            login(request, user)

            if next_url and next_url not in ['/', 'None']:
                return redirect(next_url)

            if user.is_superuser or user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'provider':
                return redirect('provider_dashboard')

            else:
                return redirect('home')

        else:
            messages.error(request, "❌ Invalid username or password.")

    return render(request, 'users/login.html', {'next': next_url})


# =========================
# ✅ USER DASHBOARD
# =========================
@login_required
def user_dashboard(request):

    if request.user.role != 'customer':
        return redirect('home')

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'users/dashboard.html', {
        'bookings': bookings
    })


# =========================
# ❌ CANCEL BOOKING
# =========================
@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(Booking, id=id, user=request.user)

    if booking.status in ['completed', 'cancelled']:
        messages.warning(request, "⚠️ This booking cannot be cancelled.")
        return redirect('user_dashboard')

    booking.status = 'cancelled'
    booking.save()

    if booking.provider:
        booking.provider.is_available = True
        booking.provider.save()

    messages.success(request, "❌ Booking cancelled successfully!")

    return redirect('user_dashboard')


# =========================
# ✅ LOGOUT
# =========================
def logout_view(request):
    logout(request)
    messages.info(request, "👋 Logged out successfully.")
    return redirect('home')