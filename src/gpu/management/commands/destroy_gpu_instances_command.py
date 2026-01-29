from django.core.management.base import BaseCommand

from src.chat.services.idle_messaging.idle_messaging_service import IdleMessagingService
from src.gpu.services.destroy_gpu_service import DestroyGpuService


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idle_messaging_service = IdleMessagingService()
        self.destroy_gpu_service = DestroyGpuService()

    def handle(self, *args, **options):
        if self.idle_messaging_service.is_messaging_idle():
            self.destroy_gpu_service.destroy_all_instance()
