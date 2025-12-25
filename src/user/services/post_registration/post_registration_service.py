import bugsnag
from django.contrib.auth.models import Group

from chatapp import settings
from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile, User

class PostRegistrationService():
    def post_register(self, user: User, invited_by_username: str | None = None):
        UserProfile.objects.create(user=user)
        Balance.objects.create(user=user)

