class GpuValueObject:
    def __init__(
            self,
            offer_id: int,
            gpu_name: str,
            gpu_ram: int,
    ):
        self.offer_id = offer_id
        self.gpu_name = gpu_name
        self.gpu_ram = gpu_ram
