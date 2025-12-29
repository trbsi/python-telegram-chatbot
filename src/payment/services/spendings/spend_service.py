from decimal import Decimal

from src.payment.exceptions import BalanceTooLowException
from src.payment.models import Balance, Spending
from src.user.models import User


class SpendService:
    def _spend(
            self,
            spender: User,
            recipient: User,
            amount: Decimal,
            object
    ) -> Decimal:
        spender_balance = Balance.objects.get(user=spender)
        recipient_balance = Balance.objects.get(user=recipient)

        if spender_balance.balance < amount:
            raise BalanceTooLowException('Balance too low.')

        spender_balance.balance = spender_balance.balance - amount
        spender_balance.save()

        recipient_balance.balance = recipient_balance.balance + amount
        recipient_balance.save()

        Spending.objects.create(
            by_user=spender,
            on_user=recipient,
            amount=amount,
            content_object=object
        )

        return amount
