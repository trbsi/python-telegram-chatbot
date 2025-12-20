import bugsnag
import stripe

from protectapp import settings
from src.payment.enums import PaymentEnum
from src.payment.value_objects.payment_webhook_value_object import PaymentWebhookValueObject


class StripeWebhookService():
    # https://docs.stripe.com/webhooks
    def handle_webhook(self, data: dict):
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        stripe.api_key = settings.STRIPE_API_KEY

        try:
            event = stripe.Event.construct_from(data, stripe.api_key)
        except ValueError as e:
            bugsnag.notify(e)
            raise e

        # @TODO maybe later
        """
        if endpoint_secret:
            # Only verify the event if you've defined an endpoint secret
            # Otherwise, use the basic event deserialized with JSON
            sig_header = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except stripe.error.SignatureVerificationError as e:
                print('⚠️  Webhook signature verification failed.' + str(e))
                return jsonify(success=False)
        """

        status = PaymentEnum.STATUS_FAILED
        if event.type == "checkout.session.completed":
            status = PaymentEnum.STATUS_SUCCESS
        elif event.type == "checkout.session.async_payment_pending":
            status = PaymentEnum.STATUS_PENDING
        elif event.type == "checkout.session.async_payment_failed":
            status = PaymentEnum.STATUS_FAILED
        elif event.type == "checkout.session.expired":
            status = PaymentEnum.STATUS_FAILED

        stripe_object = event.data.object
        metadata = stripe_object.metadata

        return PaymentWebhookValueObject(metadata.get('payment_id'), status)
