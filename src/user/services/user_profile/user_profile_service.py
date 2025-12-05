from src.user.models import User


class UserProfileService:
    def get_user_by_username(self, username: str) -> User:
        return User.objects.get(username=username)
