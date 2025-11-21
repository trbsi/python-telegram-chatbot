from django.contrib.auth.models import Group

from src.user.enum import UserEnum


class GroupSeeder:
    @staticmethod
    def seed():
        Group.objects.create(name=UserEnum.ROLE_ADMIN.value)
        Group.objects.create(name=UserEnum.ROLE_USER.value)
        Group.objects.create(name=UserEnum.ROLE_CREATOR.value)
