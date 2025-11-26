from django.core.paginator import Paginator, Page

from src.media.enums import MediaEnum
from src.media.models import Media
from src.user.models import User


class MyContentService:
    PER_PAGE = 25

    def list_my_content(self, user: User, current_page: int) -> Page[Media]:
        media = (
            Media.objects
            .filter(user=user)
            .exclude(status=MediaEnum.STATUS_DELETED.value)
            .order_by('-id')
        )
        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        return page
