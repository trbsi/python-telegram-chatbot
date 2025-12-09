from django.urls import path

from . import views

urlpatterns = [
    path('become-creator', views.become_creator, name='age_verification.become_creator'),
    path('creator-agreement', views.creator_agreement, name='age_verification.creator_agreement'),
    path('start-age-verification', views.start_age_verification, name='age_verification.start_age_verification'),
    path('webhook-age-verification', views.webhook_age_verification, name='age_verification.webhook_age_verification'),
    path('country-restricted', views.country_restricted, name='age_verification.country_restricted'),
]
