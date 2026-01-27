import requests

from chatapp import settings


class DestroyVastGpuService():
    def destroy_instance(self, instance_id: int) -> None:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.delete(f"{settings.VAST_API_BASE_URL}/instances/{instance_id}", headers=HEADERS)
        r.raise_for_status()
