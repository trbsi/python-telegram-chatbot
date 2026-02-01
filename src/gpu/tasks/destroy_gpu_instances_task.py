from celery import shared_task
from django.core.management import call_command


@shared_task
def destroy_gpu_instances_task():
    call_command('destroy_gpu_instances_command')
