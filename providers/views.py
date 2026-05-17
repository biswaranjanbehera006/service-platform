from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from bookings.models import Booking
from providers.models import Provider


# =========================================
# 🔐 HELPER: GET PROVIDER
# =========================================
def get_provider(user):

    try:

        return Provider.objects.get(user=user)

    except Provider.DoesNotExist:

        return None


# =========================================
# 📊 PROVIDER DASHBOARD
# =========================================
@login_required
def provider_dashboard(request):

    # 🔒 ONLY PROVIDER
    if request.user.role != 'provider':

        messages.error(
            request,
            "Access denied."
        )

        return redirect('home')

    # 🔥 GET PROVIDER
    provider = get_provider(request.user)

    # ❌ NO PROFILE
    if not provider:

        messages.error(
            request,
            "Provider profile not found."
        )

        return redirect('home')

    # ❌ NOT VERIFIED
    if not provider.is_verified:

        return render(
            request,
            'providers/pending_approval.html'
        )

    # =========================================
    # 📦 BOOKINGS
    # =========================================
    bookings = Booking.objects.filter(
        provider=provider
    ).order_by('-created_at')

    # =========================================
    # 📊 ANALYTICS
    # =========================================
    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status='pending'
    ).count()

    accepted_bookings = bookings.filter(
        status='accepted'
    ).count()

    completed_bookings = bookings.filter(
        status='completed'
    ).count()

    rejected_bookings = bookings.filter(
        status='rejected'
    ).count()

    total_earnings = bookings.filter(
        status='completed',
        payment_status='success'
    ).count() * 500

    recent_bookings = bookings[:5]

    # =========================================
    # 🎯 CONTEXT
    # =========================================
    context = {

        'provider': provider,

        'bookings': bookings,

        'recent_bookings': recent_bookings,

        'total_bookings': total_bookings,

        'pending_bookings': pending_bookings,

        'accepted_bookings': accepted_bookings,

        'completed_bookings': completed_bookings,

        'rejected_bookings': rejected_bookings,

        'total_earnings': total_earnings,
    }

    return render(
        request,
        'providers/dashboard.html',
        context
    )


# =========================================
# ✅ ACCEPT BOOKING
# =========================================
@login_required
def accept_booking(request, id):

    # 🔒 ONLY PROVIDER
    if request.user.role != 'provider':

        messages.error(
            request,
            "Access denied."
        )

        return redirect('home')

    # 🔥 GET PROVIDER
    provider = get_provider(request.user)

    # 🔥 GET BOOKING
    booking = get_object_or_404(

        Booking,

        id=id,

        provider=provider
    )

    # ❌ ALREADY PROCESSED
    if booking.status != 'pending':

        messages.warning(

            request,

            "This booking is already processed."
        )

        return redirect(
            'provider_dashboard'
        )

    # ✅ ACCEPT
    booking.status = 'accepted'

    booking.save()

    # 🔥 PROVIDER BUSY
    provider.is_available = False

    provider.save()

    messages.success(

        request,

        "Booking accepted successfully!"
    )

    return redirect(
        'provider_dashboard'
    )


# =========================================
# ❌ REJECT BOOKING
# =========================================
@login_required
def reject_booking(request, id):

    # 🔒 ONLY PROVIDER
    if request.user.role != 'provider':

        messages.error(
            request,
            "Access denied."
        )

        return redirect('home')

    # 🔥 GET PROVIDER
    provider = get_provider(request.user)

    # 🔥 GET BOOKING
    booking = get_object_or_404(

        Booking,

        id=id,

        provider=provider
    )

    # ❌ ALREADY PROCESSED
    if booking.status != 'pending':

        messages.warning(

            request,

            "This booking is already processed."
        )

        return redirect(
            'provider_dashboard'
        )

    # ❌ REJECT
    booking.status = 'rejected'

    booking.save()

    # 🔥 AVAILABLE AGAIN
    provider.is_available = True

    provider.save()

    messages.error(

        request,

        "Booking rejected."
    )

    return redirect(
        'provider_dashboard'
    )


# =========================================
# ✅ COMPLETE BOOKING
# =========================================
@login_required
def complete_booking(request, id):

    # 🔒 ONLY PROVIDER
    if request.user.role != 'provider':

        messages.error(
            request,
            "Access denied."
        )

        return redirect('home')

    # 🔥 GET PROVIDER
    provider = get_provider(request.user)

    # 🔥 GET BOOKING
    booking = get_object_or_404(

        Booking,

        id=id,

        provider=provider
    )

    # ❌ ONLY ACCEPTED
    if booking.status != 'accepted':

        messages.warning(

            request,

            "Only accepted bookings can be completed."
        )

        return redirect(
            'provider_dashboard'
        )

    # ✅ COMPLETE
    booking.status = 'completed'

    booking.save()

    # 🔥 AVAILABLE AGAIN
    provider.is_available = True

    provider.save()

    messages.success(

        request,

        "Booking marked as completed!"
    )

    return redirect(
        'provider_dashboard'
    )


# =========================================
# 🌟 BECOME PROVIDER PAGE
# =========================================
def become_provider(request):

    return render(
        request,
        'providers/become_provider.html'
    )