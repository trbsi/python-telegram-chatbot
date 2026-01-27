from django.db import models


class GpuInstance(models.Model):
    id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=32)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    price_per_hour = models.FloatField(null=True, blank=True)

    objects = models.Manager()

    def get_endpoint(self):
        return f'http://{self.ip_address}:{self.port}'
