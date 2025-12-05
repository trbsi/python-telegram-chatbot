from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from src.media.models import Media
from src.report.enums import ReportEnum
from src.user.models import User


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField()
    # These two are required for GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.CharField(max_length=20, choices=ReportEnum.statuses())
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def is_user(self):
        return isinstance(self.content_object, User)

    def is_media(self):
        return isinstance(self.content_object, Media)
