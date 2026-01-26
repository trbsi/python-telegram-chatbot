from django.core.management import call_command
from celery import shared_task


@shared_task
def create_gpu_task():
    call_command('ensure_gpu_running_command')
