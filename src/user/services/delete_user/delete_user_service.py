import random
import string

from src.user.models import User, UserProfile


class DeleteUserService:
    def delete_user(self, user: User) -> None:
        length = 10
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
