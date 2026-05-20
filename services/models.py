from django.db import models

# ☁️ CLOUDINARY
from cloudinary.models import CloudinaryField


# =========================================
# 📂 CATEGORY MODEL
# =========================================
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name


# =========================================
# 🛠 SERVICE MODEL
# =========================================
class Service(models.Model):

    # 🔗 CATEGORY RELATION
    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE,

        related_name='services'
    )

    # 📌 BASIC INFO
    name = models.CharField(

        max_length=100
    )

    description = models.TextField(

        blank=True,

        null=True
    )

    # 💰 PRICE
    price = models.FloatField()

    # ☁️ CLOUDINARY IMAGE
    image = CloudinaryField(

        'image',

        blank=True,

        null=True
    )

    # ✅ STATUS
    is_active = models.BooleanField(

        default=True
    )

    # ⏱ TIMESTAMPS
    created_at = models.DateTimeField(

        auto_now_add=True
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    # =========================================
    # 🔥 STRING REPRESENTATION
    # =========================================
    def __str__(self):

        return self.name