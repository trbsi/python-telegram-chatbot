import bugsnag
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.dispatch import receiver

from protectapp import settings
from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile
from src.user.services.invitation.invitation_service import InvitationService


@receiver(user_signed_up)
def after_registration(request, user, **kwargs):
    UserProfile.objects.create(user=user)
    Balance.objects.create(user=user)

    try:
        invited_by_username = request.COOKIES.get('invited_by_cookie')
        if invited_by_username:
            invitation_service = InvitationService()
            invitation_service.save_invitation(invited_by_username=invited_by_username, invited_user=user)
            if settings.IS_IN_BETA:
                creator_role: Group = Group.objects.get(name=UserEnum.ROLE_CREATOR.value)
                creator_role.user_set.add(user)
    except Exception as e:
        bugsnag.notify(e)
