from django.db import models


class GpuInstance(models.Model):
    id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=32)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
