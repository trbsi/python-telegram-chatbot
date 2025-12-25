from django.db import models

from chatapp import settings


# instance: UserProfile
def profile_image_upload_path(user_profile, filename: str) -> str:
    return f'user_profile/{user_profile.user_id}/{filename}'


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    media_count = models.IntegerField(default=0)
    timezone = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    state_code = models.CharField(max_length=2, null=True, blank=True)

    objects = models.Manager()
