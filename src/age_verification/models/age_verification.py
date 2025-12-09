from django.db import models

from src.user.models import User


class AgeVerification(models.Model):
    PROVIDER_DIDIT = 'didit.me'
    STATUS_VERIFIED = 'verified'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20)
    provider_session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
