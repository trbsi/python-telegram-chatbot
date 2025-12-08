from src.engagement.models import Like
from src.media.models import Media
from src.user.models import User


class LikeService():
    def toggle(self, media_id: int, user: User) -> None:
        media: Media = Media.objects.get(id=media_id)
        like: Like = Like.objects.filter(user=user, media=media)

        if like:
            like.delete()
            media.like_count = media.like_count - 1
        else:
            Like.objects.create(user=user, media=media)
            media.like_count = media.like_count + 1

        media.save()
