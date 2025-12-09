from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet

from src.core.utils import reverse_lazy_with_query
from src.media.enums.media_status_enum import MediaStatusEnum
from src.media.models import Media
from src.user.models import User


class UserMediaService:
    PER_PAGE = 9

    def get_user_media(self, current_user: User | AnonymousUser, username: str, current_page: int) -> dict:
        user: User = User.objects.get(username=username)
        media: QuerySet[Media] = (
            Media.objects
            .filter(status=MediaStatusEnum.STATUS_PAID.value)
            .filter(user=user)
            .order_by('-created_at')
        )

        # Show only APPROVED media for anyone who visits user profile
        # For current user show non-approved media also
        if current_user != user:
            media = media.filter(is_approved=True)

        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        result = []
        for media_item in page.object_list:
            destination_url = '#'
            if media_item.is_approved:
                destination_url = reverse_lazy_with_query(
                    route_name='feed.following',
                    kwargs=None,
                    query_params={'uid': user.id, 'mid': media_item.id, 'go_back': 1},
                )

            if media_item.is_video():
                thumbnail = str(media_item.get_thumbnail_url())
            else:
                thumbnail = media_item.get_file_url()

            # Update get_user_liked_media() and UserFollowingService also
            result.append({
                'id': media_item.id,
                'title': '',
                'thumbnail': thumbnail,
                'item_type': media_item.file_type,
                'destination_url': destination_url,
                'is_approved': int(media_item.is_approved),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
