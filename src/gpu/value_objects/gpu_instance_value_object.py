from chatapp import settings


class GpuInstanceValueObject:
    def __init__(
            self,
            instance_id: int,
            price_per_hour: float,
            status: str
    ):
        self.instance_id = instance_id
        self.price_per_hour = price_per_hour
        self.status = status

    def is_active(self) -> bool:
        return self.status == "running"

    def is_expensive(self) -> bool:
        return self.price_per_hour > settings.MAX_GPU_PRICE_PER_HOUR
