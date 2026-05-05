from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm
from providers.models import ProviderApplication
from bookings.models import Booking


# ✅ REGISTER
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            # 🔥 Provider application creation
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

                messages.info(request, "⏳ Your provider application is submitted. Wait for admin approval.")
            else:
                messages.success(request, "✅ Registration successful!")

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "⚠️ Please fix the errors below.")

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {
        'form': form
    })


# ✅ LOGIN (FIXED REDIRECT + PROVIDER VALIDATION)
def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:

            # 🔥 PROVIDER VALIDATION
            if user.role == 'provider':
                try:
                    application = ProviderApplication.objects.get(user=user)

                    if application.status == 'pending':
                        messages.warning(request, "⏳ Your application is under review. Please wait for approval.")
                        return redirect('login')

                    elif application.status == 'rejected':
                        messages.error(request, "❌ Your application was rejected. Contact support.")
                        return redirect('login')

                except ProviderApplication.DoesNotExist:
                    messages.error(request, "⚠️ No provider application found. Please register again.")
                    return redirect('register')

            login(request, user)

            # 🔥 FIXED NEXT REDIRECT (IMPORTANT)
            if next_url and next_url not in ['/', 'None']:
                return redirect(next_url)

            # 🔥 ROLE BASED REDIRECT (FIXED)
            if user.is_superuser or user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'provider':
                return redirect('provider_dashboard')

            else:
                return redirect('home')

        else:
            messages.error(request, "❌ Invalid username or password.")

    return render(request, 'users/login.html', {
        'next': next_url
    })


# ✅ USER DASHBOARD
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


# ❌ CANCEL BOOKING
@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(Booking, id=id, user=request.user)

    if booking.status in ['completed', 'cancelled']:
        messages.warning(request, "⚠️ This booking cannot be cancelled.")
        return redirect('user_dashboard')

    booking.status = 'cancelled'
    booking.save()

    # 🔥 Free provider
    if booking.provider:
        booking.provider.is_available = True
        booking.provider.save()

    messages.success(request, "❌ Booking cancelled successfully!")

    return redirect('user_dashboard')


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, "👋 Logged out successfully.")
    return redirect('home')