from decimal import Decimal

from django.db import models

from src.payment.utils import get_creator_balance_in_fiat
from src.user.models import User


class Balance(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def get_balance_as_number(self) -> Decimal | int:
        user: User = self.user
        if user.is_creator():
            return get_creator_balance_in_fiat(coins=self.balance).user_balance

        return self.balance

    def get_balance_as_string(self) -> str:
        user: User = self.user
        if user.is_creator():
            return f'${self.get_balance_as_number()}'
        else:
            return f'{self.get_balance_as_number()} coins'

    @staticmethod
    def get_user_balance(user: User):
        return Balance.objects.get(user=user)
