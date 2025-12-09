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
