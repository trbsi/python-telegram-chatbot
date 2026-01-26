import requests

from chatapp import settings
from src.gpu.value_objects.gpu_value_object import GpuValueObject


class FindVastGpuService:
    def find_cheapest_gpu(self, min_vram=15) -> GpuValueObject:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        body = {
            "limit": 1,  # get only the cheapest
            "type": "bid",  # cheapest type
            "rentable": {"eq": True},
            "rented": {"eq": False},
            "min_ram": min_vram,  # minimum 15GB RAM
            "order": [["price", "asc"]]  # sort by price ascending
        }

        r = requests.get(
            f"{settings.VAST_API_BASE_URL}/bundles",
            headers=HEADERS,
            json=body,
            timeout=30
        )
        r.raise_for_status()

        offers = r.json()["offers"]
        if not offers:
            raise RuntimeError("No GPU offers found")

        offer = offers[0]  # cheapest
        return GpuValueObject(
            offer["id"],
            offer["gpu_name"],
            offer["gpu_ram"],
        )
