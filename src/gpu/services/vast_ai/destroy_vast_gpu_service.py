import requests

from chatapp import settings
from src.gpu.services.vast_ai.my_vast_gpu_service import MyVastGpuService


class DestroyVastGpuService():
    def __init__(self) -> None:
        self.my_gpu_service = MyVastGpuService()

    def destroy_instance(self, instance_id: int) -> None:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.delete(f"{settings.VAST_API_BASE_URL}/instances/{instance_id}", headers=HEADERS)
        r.raise_for_status()

    def destroy_other_instance(self)->None:
        gpus = self.my_gpu_service.get_my_gpus()
        for gpu in gpus:
            self.destroy_instance(gpu['id'])
