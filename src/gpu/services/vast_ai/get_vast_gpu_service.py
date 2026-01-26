import requests

from chatapp import settings


class GetVastGpuService:
    def get_instance(self, instance_id: str):
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        r = requests.get(f"{settings.VAST_API_BASE_URL}/instances/{instance_id}", headers=HEADERS)
        r.raise_for_status()
        return r.json()
