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
        instance = r.json()['instances']
        return GpuInstanceValueObject(
            instance_id=instance['id'],
            price_per_hour=instance['search']['gpuCostPerHour'],
            status=instance['actual_status'],
            public_ip=instance['public_ipaddr'],
            port=instance['ports'][0],
        )
