import random

from src.user.models import User
from src.user.services.post_registration.post_registration_service import PostRegistrationService


class CreateUserService:
    def create_random_user(self) -> User:
        random_int = random.randint(100000, 1000000)
        user = User.objects.create_user(
            username=f'automatic{random_int}',
            email=f"automatic{random_int}@email.top",
            password=f"automatic{random_int}"
        )

        service = PostRegistrationService()
        service.post_register(user=user)

        return user
