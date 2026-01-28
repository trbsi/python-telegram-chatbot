import requests

from chatapp import settings
from src.gpu.value_objects.gpu_offer_value_object import GpuOfferValueObject


class FindVastGpuService:
    # https://docs.vast.ai/api-reference/search/search-offers
    def find_cheapest_gpu(self, min_vram=15) -> GpuOfferValueObject:
        HEADERS = {
            "Authorization": f"Bearer {settings.VAST_API_KEY}",
        }

        body = {
            "limit": 1,  # get only the cheapest
            "type": "on-demand",  # cheapest type
            "rentable": {"eq": True},
            "rented": {"eq": False},
            "gpu_ram": {"gte": min_vram * 1024},  # minimum 15GB RAM
            "order": [["dph_total", "asc"]]  # sort by price ascending
        }

        r = requests.post(
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
        return GpuOfferValueObject(
            offer["id"],
            offer["gpu_name"],
            offer["gpu_ram"],
            offer["search"]["gpuCostPerHour"],
        )
