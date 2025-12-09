from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from src.age_verification.models import AgeVerification, CreatorAgreement


# Register your models here.
@admin.register(AgeVerification)
class AgeVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'provider', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username',)


@admin.register(CreatorAgreement)
class CreatorAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'form_type', 'created_at')
    list_filter = ('user',)
    fields = (
        'user',
        'form_type',
        'form_version',
        'ip_address',
        'user_agent',
        'created_at',
        'read_agreement',
    )
    readonly_fields = ('read_agreement', 'created_at')
    search_fields = ('user__username',)

    @admin.display(description='Read agreement')
    def read_agreement(self, creator_agreement):
        return format_html(
            f'<a class="underline" href="{reverse_lazy('age_verification.creator_agreement')}">Read agreement</a>',
        )
