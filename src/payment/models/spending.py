from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from src.payment.utils import get_creator_balance_in_fiat
from src.user.models import User


class Spending(models.Model):
    id = models.BigAutoField(primary_key=True)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spent_by_user')
    on_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spent_on_user')
    amount = models.DecimalField(decimal_places=2, max_digits=10)  # coins
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # These two are required for GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = models.Manager()

    def amount_for_creator(self) -> str:
        amount = get_creator_balance_in_fiat(coins=self.amount).user_balance
        return f'{amount} $'

    def amount_for_user(self):
        return f'{self.amount} coins'
