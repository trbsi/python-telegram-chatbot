from enum import Enum


class MediaUnlockEnum(Enum):
    UNLOCK_LOCKED = 'locked'
    UNLOCK_PENDING = 'pending'
    UNLOCK_PERMANENT = 'permanent'
    UNLOCK_SESSION = 'session'
    UNLOCK_24H = '24h'

    @staticmethod
    def unlock_types() -> tuple:
        return (
            (MediaUnlockEnum.UNLOCK_PENDING.value, 'Pending'),
            (MediaUnlockEnum.UNLOCK_PERMANENT.value, 'Permanent'),
            (MediaUnlockEnum.UNLOCK_SESSION.value, 'Session'),
            (MediaUnlockEnum.UNLOCK_24H.value, '24H'),
        )

    @staticmethod
    def from_string(value: str):
        match value:
            case MediaUnlockEnum.UNLOCK_PENDING.value:
                return MediaUnlockEnum.UNLOCK_PENDING
            case MediaUnlockEnum.UNLOCK_SESSION.value:
                return MediaUnlockEnum.UNLOCK_SESSION
            case MediaUnlockEnum.UNLOCK_24H.value:
                return MediaUnlockEnum.UNLOCK_24H
            case MediaUnlockEnum.UNLOCK_PERMANENT.value:
                return MediaUnlockEnum.UNLOCK_PERMANENT
            case MediaUnlockEnum.UNLOCK_LOCKED.value:
                return MediaUnlockEnum.UNLOCK_LOCKED

    def is_locked(self) -> bool:
        return self == MediaUnlockEnum.UNLOCK_LOCKED

    def is_pending(self) -> bool:
        return self == MediaUnlockEnum.UNLOCK_PENDING

    def is_unlocked_permanent(self) -> bool:
        return self == MediaUnlockEnum.UNLOCK_PERMANENT
