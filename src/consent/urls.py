from django.urls import path

from src.consent import views

urlpatterns = [
    path('media/<int:media_id>', views.request_consent, name='consent.request_consent'),
    path('media', views.display_media_for_consent, name='consent.display_media_for_consent'),
    path('give-consent', views.give_media_consent, name='consent.give_media_consent'),
]
