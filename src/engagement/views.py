import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST, require_GET

from src.engagement.services.comment_create.create_comment_service import CreateCommentService
from src.engagement.services.comment_list.comment_list_service import CommentListService
from src.engagement.services.like.like_service import LikeService


@require_POST
def like(request: HttpRequest, media_id: int) -> JsonResponse:
    if request.user.is_anonymous:
        return JsonResponse({})

    like_service = LikeService()
    like_service.toggle(int(media_id), request.user)
    return JsonResponse({})


@require_GET
def list_comments(request: HttpRequest, media_id: int) -> JsonResponse:
    service = CommentListService()
    comments = service.list(int(media_id))
    return JsonResponse({'results': comments})


@require_POST
@login_required
def create_comment(request: HttpRequest) -> JsonResponse:
    post = json.loads(request.body)
    service = CreateCommentService()
    comment: dict = service.create_comment(
        user=request.user,
        comment_content=post.get('comment'),
        media_id=int(post.get('media_id'))
    )

    return JsonResponse(comment)


@require_POST
@login_required
# @TODO finish this
def delete_comment(request: HttpRequest, media_id: int) -> JsonResponse:
    return JsonResponse({})
