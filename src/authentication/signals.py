from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from src.user.models import UserProfile


@receiver(user_signed_up)
def after_registration(request, user, **kwargs):
    UserProfile.objects.create(user=user)
