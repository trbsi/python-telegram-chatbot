from django.db import models


class AgeVerificationCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    country_code = models.CharField(max_length=5)
    country_name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    state_name = models.CharField(max_length=30, null=True, blank=True)
    is_age_verification_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['country_code', 'state_code', 'is_age_verification_required']),
        ]

    objects = models.Manager()
