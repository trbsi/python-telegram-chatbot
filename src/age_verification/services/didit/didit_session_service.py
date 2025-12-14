# https://didit.me/
import requests
from django.urls.base import reverse_lazy

from age_verification.services.age_verification.age_verification_value_object import AgeVerificationValueObject
from protectapp import settings
from src.age_verification.models import AgeVerification
from src.user.models import User


class DiditSessionService:
    def __init__(self):
        self.config = settings.AGE_VERIFICATION_CONFIG.get(AgeVerification.PROVIDER_DIDIT)
        self.base_url = self.config['base_url']
        self.api_key = self.config['api_key']
        self.workflow_id = self.config['workflow_id']

    # https://docs.didit.me/reference/create-session-verification-sessions
    def create_session(self, user: User) -> AgeVerificationValueObject:
        url = f'{self.base_url}/v2/session/'
        callback = f'{settings.APP_URL}{reverse_lazy('age_verification.become_creator')}'

        payload = {
            'workflow_id': self.workflow_id,
            'callback': callback,
            'vendor_data': user.id,
            'language': 'en'
        }
        headers = {
            'accept': 'application/json',
            'x-api-key': self.api_key,
            'content-type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()
        return AgeVerificationValueObject(
            session_id=data.get('session_id'),
            status=data.get('status'),
            redirect_url=data.get('url'),
        )
