from django.contrib import admin
from .models import Provider, ProviderApplication


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_available', 'experience', 'rating']


@admin.register(ProviderApplication)
class ProviderApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at']
    list_filter = ['status']

    actions = ['approve_providers', 'reject_providers']

    # ✅ APPROVE ACTION
    def approve_providers(self, request, queryset):
        for application in queryset:

            # ❌ REMOVED THIS (BUG CAUSE)
            # if application.status == 'approved':
            #     continue

            # ✅ ALWAYS ensure provider exists (UPDATED)
            provider, created = Provider.objects.get_or_create(
                user=application.user
            )

            # ✅ Assign services (SAME BUT IMPORTANT)
            provider.services.set(application.services.all())

            # ✅ Update status (UPDATED: now handled separately)
            if application.status != 'approved':
                application.status = 'approved'
                application.save()

        # ✅ ADDED BETTER MESSAGE
        self.message_user(request, "Providers processed successfully (created/updated).")

    approve_providers.short_description = "Approve selected providers"

    # ❌ REJECT ACTION
    def reject_providers(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected providers rejected.")

    reject_providers.short_description = "Reject selected providers"