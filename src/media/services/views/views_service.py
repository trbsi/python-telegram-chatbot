from django.contrib.auth.models import AnonymousUser, User

from src.media.models import Media, Views


class ViewsService:
    def record_view(self, user: User | AnonymousUser, media_id: int) -> None:
        media: Media = Media.objects.get(id=media_id)
        media.view_count += 1
        media.save()

        if user.is_authenticated:
            Views.objects.create(
                media=media,
                user=user,
            )
