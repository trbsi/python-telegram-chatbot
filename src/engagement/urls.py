from django.urls import path

from . import views

urlpatterns = [
    path('api/like/media/<media_id>', views.like, name='engagement.api.like_media'),
    path('api/comments/media/<media_id>', views.list_comments, name='engagement.api.list_comments'),
    path('api/comments', views.create_comment, name='engagement.api.create_comment')
]
