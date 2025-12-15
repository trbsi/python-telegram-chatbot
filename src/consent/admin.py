from django.contrib import admin

from src.consent.models import MediaConsent


@admin.register(MediaConsent)
class MediaConsentAdmin(admin.ModelAdmin):
    list_filter = ('media', 'user')
    list_display = ('id', 'user', 'media', 'created_at')
