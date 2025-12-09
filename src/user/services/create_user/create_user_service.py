import random

from src.user.models import User, UserProfile


class CreateUserService:
    def create_random_user(self) -> User:
        random_int = random.randint(100000, 1000000)
        user = User.objects.create_user(
            username=f'automatic{random_int}',
            email=f"automatic{random_int}@email.top",
            password=f"automatic{random_int}"
        )

        UserProfile.objects.create(user=user)

        return user
