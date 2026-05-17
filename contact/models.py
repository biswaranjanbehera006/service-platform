from django.db import models


class Contact(models.Model):

    # =========================================
    # 👤 USER DETAILS
    # =========================================

    name = models.CharField(
        max_length=255
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    # =========================================
    # ⏱ TIMESTAMP
    # =========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================================
    # 🔥 STRING
    # =========================================

    def __str__(self):

        return self.name