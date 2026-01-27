import requests

from chatapp import settings
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class GetVastGpuService:
    def get_instance(self, instance_id: int) -> GpuInstanceValueObject:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.get(f"{settings.VAST_API_BASE_URL}/instances/{instance_id}", headers=HEADERS)
        r.raise_for_status()
        instance = r.json()
        return GpuInstanceValueObject(
            instance_id=instance['instances']['id'],
            price_per_hour=instance['instances']['search']['gpuCostPerHour'],
            status=instance['instances']['actual_status'],
        )
