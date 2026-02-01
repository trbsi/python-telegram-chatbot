from celery import shared_task
from django.core.management import call_command


@shared_task
def ensure_gpu_running_task():
    call_command('ensure_gpu_running_command')
