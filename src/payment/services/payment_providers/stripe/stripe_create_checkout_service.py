import uuid

import stripe
from stripe.checkout import Session

from protectapp import settings
from src.media.models import Media
from src.payment.models import PaymentHistory
from src.payment.value_objects.checkout_value_object import CheckoutValueObject


class StripeCreateCheckoutService:

    # https://docs.stripe.com/api/checkout/sessions/create?lang=python
    def create_checkout(self, payment_history: PaymentHistory) -> CheckoutValueObject:
        payment_id = str(uuid.uuid4())
        stripe.api_key = settings.STRIPE_API_KEY
        content_object: Media = payment_history.content_object
        success_url = cancel_url = content_object.public_media_url()

        session: Session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": settings.DEFAULT_CURRENCY,
                        "unit_amount": payment_history.price * 100,  # amount in cents → $5.00
                        "product_data": {
                            "name": "Unlocked Video Access",
                            "description": "One-time access to premium video",
                        },
                    },
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "payment_id": payment_id,
            },
        )

        return CheckoutValueObject(session.url, payment_id)
