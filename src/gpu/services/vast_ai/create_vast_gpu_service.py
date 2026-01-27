import requests

from chatapp import settings
from src.core.utils import full_url_for_route
from src.gpu.value_objects.gpu_instance_value_object import GpuInstanceValueObject


class CreateVastGpuService:
    def create_instance(
            self,
            offer_id: int,
            disk_gb: int,
            image: str = "nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04"
    ) -> GpuInstanceValueObject:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        payload = {
            "image": image,
            "disk": disk_gb,
            "onstart": open(f'{settings.BASE_DIR}/scripts/vast_ai_deployment.sh').read(),
            "ssh": True,
            "label": "gpu-worker",
            "env": {
                "GITHUB_REPO": settings.LLM_REPO_URL,
                "VPS_ENDPOINT": full_url_for_route('gpu.register_gpu'),
                "REGISTRATION_TOKEN": "not_used_but_just_in_case",
                "MODEL_URL": settings.MODEL_URL
            }
        }

        r = requests.put(
            f"{settings.VAST_API_BASE_URL}/asks/{offer_id}",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        r.raise_for_status()
        instance = r.json()
        return GpuInstanceValueObject(
            instance_id=instance['new_contract'],
            price_per_hour=0.0,
            status='ok'
        )
