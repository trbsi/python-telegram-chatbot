from chatapp import settings
from src.gpu.services.vast_ai.destroy_vast_gpu_service import DestroyVastGpuService


class DestroyGpuService():
    def __init__(self):
        self.vast = DestroyVastGpuService()

    def destroy_instance(self, instance_id: int) -> None:
        if settings.GPU_PROVIDER == 'vast_ai':
            self.vast.destroy_instance(instance_id)
        else:
            raise Exception("Not Implemented for provider")


    def destroy_other_instance(self) -> None:
        if settings.GPU_PROVIDER == 'vast_ai':
            self.vast.destroy_other_instance()
        else:
            raise Exception("Not Implemented for provider")
