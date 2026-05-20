from django.contrib.auth.models import AbstractUser
from django.db import models
import random

# ☁️ CLOUDINARY
from cloudinary.models import CloudinaryField


# =========================================
# 👤 CUSTOM USER MODEL
# =========================================
class User(AbstractUser):

    # 🔥 ROLE CHOICES
    ROLE_CHOICES = (

        ('customer', 'Customer'),

        ('provider', 'Provider'),

        ('admin', 'Admin'),
    )

    # =========================================
    # 👨‍💼 ROLE
    # =========================================
    role = models.CharField(

        max_length=10,

        choices=ROLE_CHOICES,

        default='customer'
    )

    # =========================================
    # 📱 PHONE NUMBER
    # =========================================
    phone = models.CharField(

        max_length=15,

        blank=True,

        null=True
    )

    # =========================================
    # ☁️ PROFILE IMAGE
    # =========================================
    profile_image = CloudinaryField(

        'profile_image',

        blank=True,

        null=True
    )

    # =========================================
    # 📧 EMAIL VERIFIED
    # =========================================
    is_email_verified = models.BooleanField(

        default=False
    )

    # =========================================
    # 🔥 STRING
    # =========================================
    def __str__(self):

        return self.username


# =========================================
# 🔐 EMAIL OTP MODEL
# =========================================
class EmailOTP(models.Model):

    # 👤 USER
    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE
    )

    # 🔢 OTP
    otp = models.CharField(

        max_length=6
    )

    # ⏱ CREATED TIME
    created_at = models.DateTimeField(

        auto_now_add=True
    )

    # =========================================
    # 🔥 GENERATE OTP
    # =========================================
    def generate_otp(self):

        self.otp = str(

            random.randint(
                100000,
                999999
            )
        )

        self.save()

    # =========================================
    # 🔥 STRING
    # =========================================
    def __str__(self):

        return f"{self.user.email} - {self.otp}"