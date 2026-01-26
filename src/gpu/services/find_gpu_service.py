from chatapp import settings
from src.gpu.services.vast_ai.find_vast_gpu_service import FindVastGpuService
from src.gpu.value_objects.gpu_value_object import GpuValueObject


class FindGpuService:
    def __init__(self):
        self.vast = FindVastGpuService()

    def find_cheapest_gpu(self, min_vram=15) -> GpuValueObject:
        if settings.GPU_PROVIDER == 'vast_ai':
            return self.vast.find_cheapest_gpu(min_vram)
        else:
            raise Exception("Not Implemented for provider")
