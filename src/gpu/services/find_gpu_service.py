from chatapp import settings
from src.gpu.services.vast_ai.find_vast_gpu_service import FindVastGpuService
from src.gpu.value_objects.gpu_offer_value_object import GpuOfferValueObject


class FindGpuService:
    def __init__(self):
        self.vast = FindVastGpuService()

    def find_cheapest_gpu(self, min_vram=15) -> GpuOfferValueObject:
        if settings.GPU_PROVIDER == 'vast_ai':
            return self.vast.find_cheapest_gpu(min_vram)
        else:
            raise Exception("Not Implemented for provider")
