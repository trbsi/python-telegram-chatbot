from django.db import models

from src.user.models import User


class CreatorAgreement(models.Model):
    FORM_CREATOR_AGREEMENT = 'creator_agreement'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form_type = models.CharField(max_length=20)
    form_version = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
