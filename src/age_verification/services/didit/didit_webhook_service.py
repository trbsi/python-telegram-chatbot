import hashlib
import hmac
import json
import traceback
from time import time

from django.http.request import HttpRequest

from app import settings
from app.log import log
from src.age_verification.models import AgeVerification


class DiditWebhookService:
    def __init__(self):
        self.config = settings.AGE_VERIFICATION_CONFIG.get(AgeVerification.PROVIDER_DIDIT)
        self.webhook_key = self.config['webhook_secret_key']

    # https://docs.didit.me/reference/webhooks
    def handle_webhook(self, request: HttpRequest) -> bool:
        try:
            # Get the raw request body as string
            body = request.body
            body_str = body.decode()
            log.info(f'Received webhook request: {body_str}')

            signature = request.headers.get("x-signature")
            timestamp = request.headers.get("x-timestamp")

            if not all([signature, timestamp, self.webhook_key]):
                log.error(
                    f'Received invalid webhook request. Body: {body_str}. Signature: {signature}. Timestamp: {timestamp}')
                return False

            if not self.verify_webhook_signature(body_str, signature, timestamp, self.webhook_key):
                log.error(
                    f'Could not verify webhook signature. Body: {body_str}. Signature: {signature}. Timestamp: {timestamp}')
                return False

            body = json.loads(body_str)
            session_id = body.get("session_id")
            status = body.get("status")
            vendor_data = body.get("vendor_data")

            age_verification = (AgeVerification
                                .objects
                                .filter(provider_session_id=session_id)
                                .filter(user_id=vendor_data)
                                .first())

            if status == 'Approved':
                status = AgeVerification.STATUS_VERIFIED

            age_verification.status = status
            age_verification.save()

            return True
        except Exception as e:
            tb_str = traceback.format_exc()
            log.error(f'Didit webhook service error: {e}. {tb_str}')
            return False

    def verify_webhook_signature(
            self,
            request_body: str,
            signature_header: str,
            timestamp_header: str,
            secret_key: str
    ) -> bool:
        """
        Verify incoming webhook signature
        """
        # Check if timestamp is recent (within 5 minutes)
        timestamp = int(timestamp_header)
        current_time = int(time())
        if abs(current_time - timestamp) > 300:  # 5 minutes
            return False

        # Calculate expected signature
        expected_signature = hmac.new(
            secret_key.encode("utf-8"),
            request_body.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Compare signatures using constant-time comparison
        return hmac.compare_digest(signature_header, expected_signature)
