import requests

from chatapp import settings
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class MyVastGpuService:
    # https://docs.vast.ai/api-reference/instances/show-instances
    def get_my_gpu(self) -> GpuInstanceValueObject:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.get(f"{settings.VAST_API_BASE_URL}/instances", headers=HEADERS)
        r.raise_for_status()
        instance = r.json()['instances'][0]
        ports = instance['ports'] if 'ports' in instance else {}

        return GpuInstanceValueObject(
            instance_id=instance['id'],
            price_per_hour=instance['search']['gpuCostPerHour'],
            status=instance['actual_status'],
            public_ip=instance['public_ipaddr'],
            port=self._get_port(ports),
        )

    # https://docs.vast.ai/api-reference/instances/show-instances
    def get_my_gpus(self) -> list:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.get(f"{settings.VAST_API_BASE_URL}/instances", headers=HEADERS)
        r.raise_for_status()
        instances = r.json()['instances']
        return instances

    def _get_port(self, ports: dict) -> int:
        for key, mapping in ports.items():
            if key == '22/tcp':
                continue

            host_port = mapping[0]['HostPort']
            if host_port and host_port.startswith('80'):
                return int(host_port)

        return 0
