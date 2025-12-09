from src.media.enums.media_status_enum import MediaStatusEnum

from src.media.models import Media
from src.user.tasks import task_delete_user_media


class DeleteMediaCron:
    def delete_media(self):
        media = (
            Media.objects
            .filter(status=MediaStatusEnum.STATUS_DELETED.value)
            .values('user_id')
            .distinct()
        )
        for single_media in media:
            task_delete_user_media.delay(user_id=single_media['user_id'])
