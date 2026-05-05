from django.db import models
from django.conf import settings
from services.models import Service
from providers.models import Provider

User = settings.AUTH_USER_MODEL


class Booking(models.Model):

    # 🔥 STATUS OPTIONS
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # 👤 CUSTOMER
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_bookings'
    )

    # 🛠 SERVICE
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_bookings'
    )

    # 👨‍🔧 PROVIDER
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='provider_bookings'
    )

    # 📅 BOOKING DETAILS
    date = models.DateField()
    time = models.TimeField()
    address = models.TextField()

    # ⭐ NEW — RATING (1 to 5)
    rating = models.IntegerField(
        null=True,
        blank=True
    )

    # 💬 NEW — REVIEW / COMMENT
    review = models.TextField(
        null=True,
        blank=True
    )

    # 📌 STATUS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ⏱ TRACKING
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🧠 HELPER METHODS
    def is_pending(self):
        return self.status == 'pending'

    def is_accepted(self):
        return self.status == 'accepted'

    def is_completed(self):
        return self.status == 'completed'

    def is_rated(self):
        return self.rating is not None

    def __str__(self):
        return f"{self.user} - {self.service} ({self.status})"