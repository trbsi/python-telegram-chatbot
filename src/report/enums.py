from enum import Enum
from typing import Tuple


class ReportEnum(Enum):
    TYPE_USER = 'user'
    TYPE_MEDIA = 'media'

    STATUS_PENDING = 'pending'
    STATUS_RESOLVED = 'resolved'

    @staticmethod
    def types() -> Tuple:
        return (
            (ReportEnum.TYPE_USER.value, 'User'),
            (ReportEnum.TYPE_MEDIA.value, 'Media'),
        )

    @staticmethod
    def statuses() -> Tuple:
        return (
            (ReportEnum.STATUS_PENDING.value, 'Pending'),
            (ReportEnum.STATUS_RESOLVED.value, 'Resolved'),
        )
