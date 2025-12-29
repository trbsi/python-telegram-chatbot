import random
from decimal import Decimal

from chatapp import settings
from src.core.utils import reverse_lazy_with_query
from src.payment.enums import PaymentEnum
from src.payment.models import PaymentHistory
from src.payment.services.payment_providers.ccbill.ccbill_create_checkout_service import CCBillCreateCheckoutService
from src.payment.services.payment_providers.ccbill.ccbill_webhook_service import CCBillWebhookService
from src.payment.services.payment_providers.stripe.stripe_create_checkout_service import StripeCreateCheckoutService
from src.payment.services.payment_providers.stripe.stripe_webhook_service import StripeWebhookService
from src.payment.value_objects.checkout_value_object import CheckoutValueObject
from src.payment.value_objects.payment_webhook_value_object import PaymentWebhookValueObject


class PaymentProviderService():
    def __init__(
            self,
            ccbill_create_checkout_service: CCBillCreateCheckoutService | None = None,
            ccbill_webhook_service: CCBillWebhookService | None = None,
            stripe_create_checkout_service: StripeCreateCheckoutService | None = None,
            stripe_webhook_service: StripeWebhookService | None = None,
    ):
        self.default_payment_provider = settings.DEFAULT_PAYMENT_PROVIDER
        self.ccbill_create_checkout_service = ccbill_create_checkout_service or CCBillCreateCheckoutService()
        self.ccbill_webhook_service = ccbill_webhook_service or CCBillWebhookService()
        self.stripe_create_checkout_service = stripe_create_checkout_service or StripeCreateCheckoutService()
        self.stripe_webhook_service = stripe_webhook_service or StripeWebhookService()

    def create_checkout(self, payment_history: PaymentHistory) -> CheckoutValueObject:
        if self.default_payment_provider == PaymentEnum.PROVIDER_DUMMY.value:
            payment_id = str(random.randint(100000, 1000000))
            return CheckoutValueObject(
                reverse_lazy_with_query('payment.webhook', query_params={'payment_id': payment_id}),
                payment_id
            )
        elif self.default_payment_provider == PaymentEnum.PROVIDER_CCBILL.value:
            return self.ccbill_create_checkout_service.create_checkout(payment_history)
        elif self.default_payment_provider == PaymentEnum.PROVIDER_STRIPE.value:
            return self.stripe_create_checkout_service.create_checkout(payment_history)

        raise Exception('Payment provider is not supported for checkout.')

    def handle_webook(self, query_params: dict, body: dict) -> PaymentWebhookValueObject:
        if self.default_payment_provider == PaymentEnum.PROVIDER_DUMMY.value:
            return PaymentWebhookValueObject(query_params.get('payment_id'), PaymentEnum.STATUS_SUCCESS.value)
        elif self.default_payment_provider == PaymentEnum.PROVIDER_CCBILL.value:
            return self.ccbill_webhook_service.handle_webhook(body)
        elif self.default_payment_provider == PaymentEnum.PROVIDER_STRIPE.value:
            return self.stripe_webhook_service.handle_webhook(body)

        raise Exception('Payment provider is not supported for webhook.')
