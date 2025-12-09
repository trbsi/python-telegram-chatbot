from django.db import models

from src.payment.enums import PaymentEnum
from src.user.models import User


class Payout(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.CharField(max_length=10, choices=PaymentEnum.providers())
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
