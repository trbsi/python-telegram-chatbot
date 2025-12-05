from django.urls import path

from . import views

urlpatterns = [
    path('api/get-media', views.api_get_user_media, name='user.api.get_media'),
    path('<str:username>', views.profile, name='user.profile'),
]
