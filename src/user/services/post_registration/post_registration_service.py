import bugsnag
from django.contrib.auth.models import Group

from protectapp import settings
from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile, User
from src.user.services.invitation.invitation_service import InvitationService


class PostRegistrationService():
    def post_register(self, user: User, invited_by_username: str | None = None):
        UserProfile.objects.create(user=user)
        Balance.objects.create(user=user)

        try:
            if invited_by_username:
                invitation_service = InvitationService()
                invitation_service.save_invitation(invited_by_username=invited_by_username, invited_user=user)
                if settings.IS_IN_BETA:
                    creator_role: Group = Group.objects.get(name=UserEnum.ROLE_CREATOR.value)
                    creator_role.user_set.add(user)
        except Exception as e:
            bugsnag.notify(e)
