from django.core.management.base import BaseCommand

from src.chat.services.idle_messaging.idle_messaging_service import IdleMessagingService
from src.gpu.models import GpuInstance
from src.gpu.services.destroy_gpu_service import DestroyGpuService


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idle_messaging_service = IdleMessagingService()
        self.destroy_gpu_service = DestroyGpuService()

    def handle(self, *args, **options):
        running_gpu = GpuInstance.objects.filter(status=GpuInstance.STATUS_RUNNING).count()

        if running_gpu > 0 and self.idle_messaging_service.is_messaging_idle():
            self.destroy_gpu_service.destroy_all_instance()
            GpuInstance.objects.all().delete()

        gpu_instance: GpuInstance = GpuInstance.objects.filter(status=GpuInstance.STATUS_CREATING).first()
        if gpu_instance is not None and gpu_instance.time_diff() >= 600:  # 10 minutes
            self.destroy_gpu_service.destroy_instance(gpu_instance.instance_id)
            gpu_instance.delete()
