from django.db import models
from django.db.models import Manager

from src.user.models import User


class Invitation(models.Model):
    FEATURE_ACTIVE = True
    MAX_INVITES = 10

    id = models.AutoField(primary_key=True)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_user')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_by_user')
    registered_at = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    @staticmethod
    def invitations_left(user: User) -> int:
        return Invitation.MAX_INVITES - Invitation.objects.filter(invited_by=user).count()
