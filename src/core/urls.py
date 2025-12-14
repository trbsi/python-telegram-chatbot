from django.urls import path

from src.media import views as media_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.landing_page, name='about'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('legal-documents', views.legal_documents, name='legal_documents'),
    path('contact', views.contact, name='contact'),
    path('v/<int:id>', media_views.view_single_media, name='media.view_single_media'),
]
