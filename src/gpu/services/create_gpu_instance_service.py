from chatapp import settings
from src.gpu.services.vast_ai.create_vast_gpu_service import CreateVastGpuService
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class CreateGpuInstanceService:
    def __init__(self):
        self.vast = CreateVastGpuService()

    def create_instance(
            self,
            offer_id: int,
            disk_gb: int | None = None,
            image: str | None = None
    ) -> GpuInstanceValueObject:
        if disk_gb is None:
            disk_gb = settings.GPU_DISK_GB

        if settings.GPU_PROVIDER == 'vast_ai':
            return self.vast.create_instance(offer_id, disk_gb, image)
        else:
            raise Exception("Not Implemented for provider")
