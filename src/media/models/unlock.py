from django.db import models

from src.media.enums.media_unlock_enum import MediaUnlockEnum
from src.media.models import Media
from src.user.models import User


class Unlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unlock_type = models.CharField(max_length=20, choices=MediaUnlockEnum.unlock_types())

    objects = models.Manager()
