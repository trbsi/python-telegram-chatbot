from django.urls import path

from . import views

urlpatterns = [
    path('delete', views.delete, name='user.delete'),
    path('do-delete', views.do_delete, name='user.do_delete'),

    path('<str:username>', views.profile, name='user.profile'),
]
