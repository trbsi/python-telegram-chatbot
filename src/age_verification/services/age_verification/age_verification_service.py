from django.http.request import HttpRequest

from protectapp import settings
from src.age_verification.models import AgeVerification
from src.age_verification.services.didit.didit_session_service import DiditSessionService
from src.age_verification.services.didit.didit_webhook_service import DiditWebhookService
from src.user.models import User


class AgeVerificationService:
    def is_didit(self):
        return settings.AGE_VERIFICATION_PROVIDER == AgeVerification.PROVIDER_DIDIT

    def start_verification(self, user: User) -> str:
        if self.is_didit():
            service = DiditSessionService()
            result = service.create_session(user)
            provider = AgeVerification.PROVIDER_DIDIT
        else:
            raise Exception('No available age verification providers')

        AgeVerification.objects.create(
            user=user,
            provider=provider,
            provider_session_id=result.get('session_id'),
            status=result.get('status'),
        )

        return result.get('redirect_url')

    def finish_verification(self, request: HttpRequest) -> bool:
        if self.is_didit():
            service = DiditWebhookService()
            return service.handle_webhook(request)
        else:
            raise Exception('No available age verification providers')
