from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q  # 🔥 for smart matching

from .forms import BookingForm
from .models import Booking
from providers.models import Provider


# ✅ CREATE BOOKING (SMART AUTO ASSIGN PROVIDER)
@login_required
def create_booking(request):

    if request.user.role != 'customer':
        messages.error(request, "❌ Only customers can create bookings.")
        return redirect('home')

    service_id = request.GET.get('service')

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            service = booking.service

            # 🔥 SMART PROVIDER MATCHING
            providers = Provider.objects.filter(
                services=service,
                is_available=True
            ).annotate(
                active_jobs=Count(
                    'provider_bookings',
                    filter=Q(provider_bookings__status__in=['pending', 'accepted'])
                )
            ).order_by(
                'active_jobs',     # least busy first
                '-rating',         # higher rating first
                '-experience'      # more experience first
            )

            if not providers.exists():
                messages.error(request, "❌ No provider available for this service right now.")
                return redirect('home')

            provider = providers.first()

            booking.provider = provider
            booking.status = 'pending'
            booking.save()

            # 🔥 mark provider busy
            provider.is_available = False
            provider.save()

            messages.success(request, f"✅ Booking created! Assigned to {provider.user.username}")

            return redirect('user_dashboard')

        else:
            messages.error(request, "⚠️ Please correct the errors below.")

    else:
        form = BookingForm()

        # Pre-select service if coming from service page
        if service_id:
            form.fields['service'].initial = service_id

    return render(request, 'bookings/booking_form.html', {
        'form': form
    })


# ✅ UPDATE BOOKING STATUS (PROVIDER ACTION)
@login_required
def update_booking_status(request, booking_id, status):

    booking = get_object_or_404(Booking, id=booking_id)

    # 🔐 SECURITY CHECK
    if not booking.provider or booking.provider.user != request.user:
        messages.error(request, "❌ You are not authorized to update this booking.")
        return redirect('home')

    allowed_status = ['accepted', 'rejected', 'completed']

    if status not in allowed_status:
        messages.error(request, "⚠️ Invalid status update.")
        return redirect('provider_dashboard')

    # 🔥 STATUS FLOW CONTROL
    if booking.status == 'pending' and status in ['accepted', 'rejected']:
        booking.status = status

        # 🔥 If rejected → free provider
        if status == 'rejected':
            booking.provider.is_available = True
            booking.provider.save()

    elif booking.status == 'accepted' and status == 'completed':
        booking.status = status

        # 🔥 After completion → provider free again
        booking.provider.is_available = True
        booking.provider.save()

    else:
        messages.warning(request, "⚠️ Invalid status transition.")
        return redirect('provider_dashboard')

    booking.save()

    messages.success(request, f"✅ Booking {status} successfully!")

    return redirect('provider_dashboard')






@login_required
def rate_booking(request, id):

    booking = get_object_or_404(Booking, id=id, user=request.user)

    # Only completed bookings can be rated
    if booking.status != 'completed':
        messages.error(request, "You can only rate completed bookings.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review = request.POST.get('review')

        booking.rating = rating
        booking.review = review
        booking.save()

        # 🔥 Update provider rating
        provider = booking.provider
        all_ratings = Booking.objects.filter(
            provider=provider,
            rating__isnull=False
        )

        avg = sum(b.rating for b in all_ratings) / all_ratings.count()
        provider.rating = round(avg, 1)
        provider.save()

        messages.success(request, "Thanks for your feedback ⭐")
        return redirect('user_dashboard')

    return render(request, 'bookings/rate.html', {'booking': booking})