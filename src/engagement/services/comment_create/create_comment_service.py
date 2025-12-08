from django.contrib.auth.models import AnonymousUser
from django.db import transaction

from src.core.utils import format_datetime
from src.engagement.models import Comment
from src.media.models import Media
from src.payment.services.spendings.spend_service import SpendService
from src.user.models import User


class CreateCommentService():
    def __init__(self, spend_service: SpendService | None = None):
        self.spend_service = spend_service or SpendService()

    @transaction.atomic
    def create_comment(self, user: AnonymousUser | User, comment_content: str, media_id: int) -> dict:
        if user.is_authenticated == False:
            raise Exception("You are not authenticated")

        media = Media.objects.get(id=media_id)
        comment = Comment.objects.create(user=user, media=media, comment=comment_content)
        media.comment_count = media.comment_count + 1
        media.save()

        self.spend_service.spend_comment(user, comment)

        return {
            'id': comment.id,
            'text': comment.comment,
            'created_at': format_datetime(comment.created_at),
            'user': {
                'username': comment.user.username,
                'avatar': comment.user.get_profile_picture(),
            }
        }
