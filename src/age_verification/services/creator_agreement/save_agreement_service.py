from src.age_verification.models import CreatorAgreement
from src.user.models import User


class SaveAgreementService():
    def save_agreement(self, user: User, ip: str, user_agent: str):
        CreatorAgreement.objects.create(
            user=user,
            form_type=CreatorAgreement.FORM_CREATOR_AGREEMENT,
            form_version=1,
            ip_address=ip,
            user_agent=user_agent,
        )
