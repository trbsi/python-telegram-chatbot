from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.user.models import User
from src.user.services.delete_user.delete_user_service import DeleteUserService
from src.user.services.user_media.user_media_service import UserMediaService
from src.user.services.user_profile.user_profile_service import UserProfileService


# Create your views here.
# ------------------- USER PROFILE HOMEPAGE ------------------------
@require_GET
def profile(request: HttpRequest, username: str) -> HttpResponse:
    logged_in_user = request.user
    user_profile_service = UserProfileService()
    current_user: User = user_profile_service.get_user_by_username(username)

    if current_user.is_regular_user() and current_user.username != logged_in_user.username:
        raise Http404

    is_the_same_user = logged_in_user.id == current_user.id
    media_api_url = reverse_lazy('user.api.get_media')

    return render(request, 'profile.html', {
        'is_the_same_user': is_the_same_user,
        'current_user': current_user,
        'logged_in_user': logged_in_user,
        'media_api_url': media_api_url,
        'report_content_api': reverse_lazy('report.api.report_content'),
        'is_following': False
    })


@require_GET
def api_get_user_media(request: HttpRequest) -> JsonResponse:
    get = request.GET
    page = int(get.get('page'))
    username = get.get('username')
    user: User | AnonymousUser = request.user

    user_media_service = UserMediaService()
    data: dict = user_media_service.get_user_media(
        current_user=user,
        username=username,
        current_page=page
    )

    return JsonResponse({'results': data['result'], 'next_page': data['next_page']})


# ------------------- DELETE USER ------------------------
@require_GET
@login_required
def delete(request: HttpRequest) -> HttpResponse:
    return render(request, 'delete.html')


@require_POST
@login_required
def do_delete(request: HttpRequest) -> HttpResponse:
    delete_user_service = DeleteUserService()
    delete_user_service.delete_user(user=request.user)
    logout(request)
    messages.success(request=request, message='Account deleted successfully')
    return redirect(reverse_lazy('home'))
