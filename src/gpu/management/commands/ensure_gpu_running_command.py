from django.core.management.base import BaseCommand

from src.gpu.models import GpuInstance
from src.gpu.services.create_gpu_instance_service import CreateGpuInstanceService
from src.gpu.services.find_gpu_service import FindGpuService
from src.gpu.services.get_gpu_service import GetGpuService


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            gpu_instance = GpuInstance.objects.first()
            if not gpu_instance:
                raise Exception("Instance not found")

            service = GetGpuService()
            instance = service.get_instance(gpu_instance.instance_id)
            if instance["actual_status"] != "running":
                raise Exception("GPU not running")
        except Exception:
            find_gpu_service = FindGpuService()
            create_gpu_service = CreateGpuInstanceService()

            offer = find_gpu_service.find_cheapest_gpu()
            instance = create_gpu_service.create_instance(offer_id=offer.offer_id)

            print(offer)
            print(instance)
