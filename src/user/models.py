from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from protectapp import settings


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False, null=False, validators=[RegexValidator(
        r'^[0-9a-zA-Z]*$',
        'Username must contain only letters and numbers.'
    )])
    email = models.EmailField(unique=True)

    def get_profile_picture(self):
        profile_image = str(self.profile.profile_image)
        if profile_image != '' and profile_image is not None:
            return settings.MEDIA_URL + profile_image

        return f"https://ui-avatars.com/api/?name={self.username}"

    def is_regular_user(self):
        return False

    def is_creator(self):
        return True

    def get_role(self) -> str:
        return self.groups.first().name


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
