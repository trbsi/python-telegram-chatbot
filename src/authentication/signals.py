from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from src.user.services.post_registration.post_registration_service import PostRegistrationService


@receiver(user_signed_up)
def after_registration(request, user, **kwargs):
    service = PostRegistrationService()
    service.post_register(user=user, invited_by_username=request.COOKIES.get('invited_by_cookie'))
