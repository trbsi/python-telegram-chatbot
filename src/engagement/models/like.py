from django.db import models

from src.media.models import Media
from src.user.models import User as User


class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'media'], name='unique_like')
        ]
