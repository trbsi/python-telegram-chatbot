from django.db.models import QuerySet

from src.consent.models import MediaConsent
from src.media.models import Media
from src.user.models import User


class MediaConsentService:
    def attach_user_to_media(self, media_ids: list, user: User) -> None:
        media: QuerySet[Media] = Media.objects.filter(id__in=media_ids)

        for single_media in media:
            MediaConsent.objects.create(user=user, media=single_media)
