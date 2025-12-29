from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.user.models import User
from src.user.services.delete_user.delete_user_service import DeleteUserService
from src.user.services.user_profile.user_profile_service import UserProfileService


# Create your views here.
# ------------------- USER PROFILE HOMEPAGE ------------------------
@require_GET
def profile(request: HttpRequest, username: str) -> HttpResponse:
    logged_in_user = request.user
    user_profile_service = UserProfileService()
    current_user: User = user_profile_service.get_user_by_username(username)

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
