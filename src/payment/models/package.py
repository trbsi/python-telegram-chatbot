from django.db import models


class Package(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    bonus = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
