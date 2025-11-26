from django.contrib.auth.models import Group
from django.contrib.auth.models import User as User
from faker import Faker

from src.user.models import UserProfile


class UserSeeder:
    @staticmethod
    def seed():
        faker = Faker()
        for i in range(5):
            # -------- User ---------
            user = User.objects.create_user(username=f'user{i}', email=f'user{i}@mail.com', password='123456')
            user.groups.add(Group.objects.get(name='user'))
            user.save()
            UserProfile.objects.create(user=user)

            # -------- Creator ---------
            creator = User.objects.create_user(
                username=f'creator{i}',
                email=f'creator{i}@mail.com',
                password='123456'
            )
            creator.groups.add(Group.objects.get(name='creator'))
            creator.save()
            UserProfile.objects.create(user=creator)

            profile: UserProfile = creator.profile
            profile.bio = faker.text(max_nb_chars=200)
            profile.save()
