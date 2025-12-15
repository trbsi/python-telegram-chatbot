import random
import string

from django.db import transaction

from src.age_verification.models import AgeVerification, CreatorAgreement
from src.engagement.models import Comment
from src.media.enums.media_status_enum import MediaStatusEnum
from src.media.models import Media
from src.user.models import User, UserProfile
from src.user.tasks import task_delete_user_media


class DeleteUserService:
    def delete_user(self, user: User) -> None:
        length = 10
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Media
        Media.objects.filter(user=user).update(status=MediaStatusEnum.STATUS_DELETED.value)
        Comment.objects.filter(user=user).delete()

        # Age verification
        AgeVerification.objects.filter(user=user).delete()
        CreatorAgreement.objects.filter(user=user).delete()

        user.username = f"{user.id}_deleted_user"
        user.first_name = f"{user.id}_deleted_user"
        user.last_name = f"{user.id}_deleted_user"
        user.email = f"{user.id}_deleted_user@deleted.xxx"
        user.is_active = False
        user.set_password(random_string)
        user.save()

        profile: UserProfile = UserProfile.objects.get(user=user)
        profile.profile_image = None
        profile.bio = None
        profile.save()

        transaction.on_commit(lambda: task_delete_user_media.delay(user_id=user.id))
