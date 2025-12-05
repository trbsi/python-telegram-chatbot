from django.urls import path

from . import views

urlpatterns = [
    path('api/report', views.api_report, name='report.api.report_content'),
]
