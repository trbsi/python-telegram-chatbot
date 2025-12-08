from django.db import transaction

from src.media.enums import MediaEnum
from src.media.models import Media, Unlock
from src.payment.models import PaymentHistory
from src.payment.services.buy_package.buy_package_service import BuyPackageService
from src.payment.services.spendings.spend_service import SpendService
from src.user.models import User


class UnlockService():
    def __init__(
            self,
            spend_service: SpendService | None = None,
            buy_package_service: BuyPackageService | None = None
    ):
        self.spend_service = spend_service or SpendService()
        self.buy_package_service = buy_package_service or BuyPackageService()

    @transaction.atomic
    def unlock_by_balance(self, user: User, media_id: int) -> None:
        media: Media = Media.objects.get(id=media_id)
        amount = self.spend_service.spend_media_unlock(user=user, media=media)
        Unlock.objects.create(
            user=user,
            media=media,
            amount=amount,
            unlock_type=MediaEnum.UNLOCK_PERMANENT.value,
        )

    @transaction.atomic
    def unlock_by_payment(self, user: User, media_id: int) -> str:
        media: Media = Media.objects.get(id=media_id)
        checkout_value_object = self.buy_package_service.buy_custom_package(
            user=user,
            price=media.unlock_price,
            amount=media.unlock_price
        )

        unlock = Unlock.objects.create(
            user=user,
            media=media,
            amount=media.unlock_price,
            unlock_type=MediaEnum.UNLOCK_PENDING.value,
        )

        payment_history: PaymentHistory = (
            PaymentHistory.objects
            .filter(provider_payment_id=checkout_value_object.provider_payment_id)
            .first()
        )
        payment_history.content_object = unlock
        payment_history.save()

        return checkout_value_object.redirect_url
