from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from src.payment.enums import PaymentEnum
from src.user.models import User


class PaymentHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.CharField(max_length=10, choices=PaymentEnum.providers())
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=PaymentEnum.statuses())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = models.Manager()
