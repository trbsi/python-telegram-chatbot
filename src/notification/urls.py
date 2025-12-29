from django.urls import path

from . import views

urlpatterns = [
    path('api/web-push-keys', views.api_web_push_keys, name='notification.web_push_keys'),
    path('test-notifications', views.test_notifications),
]
