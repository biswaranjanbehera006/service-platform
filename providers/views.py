from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookings.models import Booking
from providers.models import Provider


# 🔐 HELPER: GET PROVIDER
def get_provider(user):
    try:
        return Provider.objects.get(user=user)
    except Provider.DoesNotExist:
        return None


# 📊 PROVIDER DASHBOARD
@login_required
def provider_dashboard(request):

    if request.user.role != 'provider':
        return redirect('home')

    provider = get_provider(request.user)

    if not provider:
        messages.error(request, "❌ Provider profile not found.")
        return redirect('home')

    bookings = Booking.objects.filter(
        provider=provider
    ).order_by('-created_at')

    return render(request, 'providers/dashboard.html', {
        'bookings': bookings
    })


# ✅ ACCEPT BOOKING
@login_required
def accept_booking(request, id):

    if request.user.role != 'provider':
        return redirect('home')

    provider = get_provider(request.user)

    booking = get_object_or_404(
        Booking,
        id=id,
        provider=provider
    )

    if booking.status != 'pending':
        messages.warning(request, "⚠️ This booking is already processed.")
        return redirect('provider_dashboard')

    booking.status = 'accepted'
    booking.save()

    # 🔥 Provider remains busy (already set at booking time)

    messages.success(request, "✅ Booking accepted successfully!")
    return redirect('provider_dashboard')


# ❌ REJECT BOOKING
@login_required
def reject_booking(request, id):

    if request.user.role != 'provider':
        return redirect('home')

    provider = get_provider(request.user)

    booking = get_object_or_404(
        Booking,
        id=id,
        provider=provider
    )

    if booking.status != 'pending':
        messages.warning(request, "⚠️ This booking is already processed.")
        return redirect('provider_dashboard')

    booking.status = 'rejected'
    booking.save()

    # 🔥 FIX: Make provider available again
    provider.is_available = True
    provider.save()

    messages.error(request, "❌ Booking rejected.")
    return redirect('provider_dashboard')


# ✅ COMPLETE BOOKING
@login_required
def complete_booking(request, id):

    if request.user.role != 'provider':
        return redirect('home')

    provider = get_provider(request.user)

    booking = get_object_or_404(
        Booking,
        id=id,
        provider=provider
    )

    if booking.status != 'accepted':
        messages.warning(request, "⚠️ Only accepted bookings can be completed.")
        return redirect('provider_dashboard')

    booking.status = 'completed'
    booking.save()

    # 🔥 FIX: Make provider available again
    provider.is_available = True
    provider.save()

    messages.success(request, "🎉 Booking marked as completed!")
    return redirect('provider_dashboard')