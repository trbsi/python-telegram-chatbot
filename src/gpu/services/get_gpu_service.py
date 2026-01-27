from chatapp import settings
from src.gpu.services.vast_ai.get_vast_gpu_service import GetVastGpuService
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class GetGpuService:
    def __init__(self):
        self.vast = GetVastGpuService()

    def get_instance(self, instance_id: int) -> GpuInstanceValueObject:
        if settings.GPU_PROVIDER == 'vast_ai':
            return self.vast.get_instance(instance_id)
        else:
            raise Exception("Not Implemented for provider")
