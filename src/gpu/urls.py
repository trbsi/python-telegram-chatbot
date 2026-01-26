from django.urls import path

from . import views

urlpatterns = [
    path('register-gpu', views.register_gpu, name='gpu.register_gpu'),
]
