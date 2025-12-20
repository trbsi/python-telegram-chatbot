from src.payment.enums import PaymentEnum


class PaymentWebhookValueObject:
    def __init__(self, provider_payment_id: str, status: PaymentEnum):
        self.provider_payment_id = provider_payment_id
        self.status = status
