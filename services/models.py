from django.db import models


# 📂 CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 🛠 SERVICE MODEL (UPDATED)
class Service(models.Model):

    # 🔗 RELATION
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='services'
    )

    # 📌 BASIC INFO
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # 💰 PRICING
    price = models.FloatField()

    # 🖼 IMAGE
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    # ⭐ OPTIONAL STATUS (FOR FUTURE CONTROL)
    is_active = models.BooleanField(default=True)

    # ⏱ TRACKING (IMPORTANT FOR ADMIN UI)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name