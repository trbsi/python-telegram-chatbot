from django.db import models
from django.db.models import Manager

from src.media.models import Media
from src.user.models import User


# Create your models here.
class MediaConsent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = Manager()
