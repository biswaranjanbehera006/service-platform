from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

from services.models import Service


User = settings.AUTH_USER_MODEL


# ✅ FINAL APPROVED PROVIDER (USED IN SYSTEM)
class Provider(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    services = models.ManyToManyField(
        Service,
        related_name='providers'
    )

    is_available = models.BooleanField(
        default=True
    )

    experience = models.PositiveIntegerField(
        help_text="Years of experience",
        default=0
    )

    rating = models.FloatField(
        default=0.0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 🧠 HELPER METHODS
    def is_busy(self):
        return not self.is_available

    def __str__(self):
        return f"{self.user.username} (Provider)"


# ✅ PROVIDER APPLICATION (FOR ADMIN APPROVAL)
class ProviderApplication(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_application'
    )

    # =========================================
    # 📄 DOCUMENTS (CLOUDINARY)
    # =========================================
    aadhar_card = CloudinaryField(
        'aadhar_card'
    )

    passport_photo = CloudinaryField(
        'passport_photo'
    )

    cv = CloudinaryField(
        'cv',
        resource_type='raw'
    )

    driving_license = CloudinaryField(
        'driving_license'
    )

    # =========================================
    # 🛠️ SERVICES
    # =========================================
    services = models.ManyToManyField(
        Service,
        related_name='applications'
    )

    # =========================================
    # 📊 STATUS
    # =========================================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # =========================================
    # ⏱ TRACKING
    # =========================================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================
    # 🧠 HELPER METHODS
    # =========================================
    def is_pending(self):
        return self.status == 'pending'

    def is_approved(self):
        return self.status == 'approved'

    def is_rejected(self):
        return self.status == 'rejected'

    def __str__(self):
        return f"{self.user.username} - {self.status}"