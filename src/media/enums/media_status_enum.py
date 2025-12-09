from enum import Enum
from typing import Tuple


class MediaStatusEnum(Enum):
    STATUS_PAID = 'paid'
    STATUS_SCHEDULE = 'schedule'
    STATUS_DELETED = 'deleted'
    STATUS_FREE = 'free'
    STATUS_PENDING = 'pending'
    STATUS_PRIVATE = 'private'

    @staticmethod
    def statuses() -> Tuple:
        return (
            (MediaStatusEnum.STATUS_FREE.value, 'Free'),
            (MediaStatusEnum.STATUS_PAID.value, 'Paid'),
            (MediaStatusEnum.STATUS_PRIVATE.value, 'Private'),
            (MediaStatusEnum.STATUS_SCHEDULE.value, 'Schedule'),
            (MediaStatusEnum.STATUS_PENDING.value, 'Pending'),
            (MediaStatusEnum.STATUS_DELETED.value, 'Deleted'),
        )
