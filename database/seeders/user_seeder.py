from django.contrib.auth.models import Group
from faker import Faker

from src.age_verification.models import AgeVerification, CreatorAgreement
from src.payment.models import Balance
from src.user.models import User as User, UserProfile


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
            Balance.objects.create(user=user)

            # -------- Creator ---------
            creator = User.objects.create_user(
                username=f'creator{i}',
                email=f'creator{i}@mail.com',
                password='123456'
            )
            creator.groups.add(Group.objects.get(name='creator'))
            creator.save()
            UserProfile.objects.create(user=creator)
            Balance.objects.create(user=creator)

            profile: UserProfile = creator.profile
            profile.bio = faker.text(max_nb_chars=200)
            profile.save()

            if i % 2 == 0:
                AgeVerification.objects.create(
                    user=creator,
                    provider=AgeVerification.PROVIDER_DIDIT,
                    provider_session_id=faker.uuid4(),
                    status=AgeVerification.STATUS_VERIFIED,
                )

                CreatorAgreement.objects.create(
                    user=creator,
                    form_type=CreatorAgreement.FORM_CREATOR_AGREEMENT,
                    form_version=1,
                    ip_address=faker.ipv4(),
                    user_agent=faker.user_agent(),
                )
