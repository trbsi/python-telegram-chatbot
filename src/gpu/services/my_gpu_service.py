from chatapp import settings
from src.gpu.services.vast_ai.my_vast_gpu_service import MyVastGpuService
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class MyGpuService:
    def __init__(self):
        self.vast = MyVastGpuService()

    def get_my_gpu(self) -> GpuInstanceValueObject:
        if settings.GPU_PROVIDER == 'vast_ai':
            return self.vast.get_my_gpu()
        else:
            raise Exception("Not Implemented for provider")