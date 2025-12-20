from protectapp import settings
from src.media.enums.media_unlock_enum import MediaUnlockEnum
from src.media.models import Unlock
from src.payment.enums import PaymentEnum
from src.payment.models import PaymentHistory, Balance, Package
from src.payment.services.payment_providers.payment_provider_service import PaymentProviderService
from src.payment.value_objects.payment_webhook_value_object import PaymentWebhookValueObject


class PaymentWebhookService:
    def __init__(self, provider_service: PaymentProviderService | None = None):
        self.payment_provider_service = provider_service or PaymentProviderService()

    # @TODO finish webhook
    def handle_webook(self, query_params: dict, body: dict) -> None | str:
        payment_status: PaymentWebhookValueObject = self.payment_provider_service.handle_webook(query_params, body)

        payment_history: PaymentHistory = (
            PaymentHistory
            .objects
            .get(provider_payment_id=payment_status.provider_payment_id)
        )
        payment_history.status = payment_status.status
        payment_history.save()

        if not payment_status.status.is_success():
            return

        foreign_object = payment_history.content_object
        if isinstance(foreign_object, Package):
            balance = Balance.objects.get(user=payment_history.user)
            balance.balance += payment_history.amount
            balance.save()

        if isinstance(foreign_object, Unlock):
            foreign_object.unlock_type = MediaUnlockEnum.UNLOCK_PERMANENT.value
            foreign_object.save()
            if settings.DEFAULT_PAYMENT_PROVIDER == PaymentEnum.PROVIDER_DUMMY.value:
                return foreign_object.media.public_media_url()
