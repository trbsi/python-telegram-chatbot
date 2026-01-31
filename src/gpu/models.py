from datetime import datetime, timezone

from django.db import models


class GpuInstance(models.Model):
    STATUS_CREATING = 'creating'
    STATUS_CREATE_NEW = 'create_new'
    STATUS_RUNNING = 'running'

    id = models.AutoField(primary_key=True)
    instance_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    price_per_hour = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def get_endpoint(self):
        return f'http://{self.ip_address}:{self.port}/reply'

    def time_diff(self):
        now = datetime.now(timezone.utc)
        return (now - self.created_at).total_seconds()
