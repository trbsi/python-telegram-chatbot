class GpuOfferValueObject:
    def __init__(
            self,
            offer_id: int,
            gpu_name: str,
            gpu_ram: int,
            price_per_hour: float
    ):
        self.offer_id = offer_id
        self.gpu_name = gpu_name
        self.gpu_ram = gpu_ram
        self.price_per_hour = price_per_hour
