from django.urls import path

from . import views

urlpatterns = [
    path('api/get-media', views.api_get_user_media, name='user.api.get_media'),
    path('delete', views.delete, name='user.delete'),
    path('do-delete', views.do_delete, name='user.do_delete'),

    path('<str:username>', views.profile, name='user.profile'),
]
