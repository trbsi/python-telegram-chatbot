import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.contrib.auth.models import AnonymousUser

from protectapp import settings
from src.engagement.models import Like, Comment
from src.media.enums.media_unlock_enum import MediaUnlockEnum
from src.media.models import Media, Unlock
from src.media.services.single_media.media_value_object import MediaValueObject
from src.user.models import User


class SingleMediaService:

    def get_single_media(self, media_id: int, user: User | AnonymousUser) -> MediaValueObject:
        media = Media.objects \
            .select_related('user') \
            .filter(id=media_id) \
            .filter(is_processed=True, is_approved=True) \
            .get()

        total_likes = Like.objects.filter(media=media).count()
        total_comments = Comment.objects.filter(media=media).count()

        if user.is_authenticated:
            if user == media.user:
                unlock_type = MediaUnlockEnum.UNLOCK_PERMANENT
            else:
                unlock = Unlock.objects.filter(user=user, media=media).first()
                unlock_type = MediaUnlockEnum.from_string(unlock.unlock_type) if unlock \
                    else MediaUnlockEnum.UNLOCK_LOCKED
            is_liked = Like.objects.filter(user=user, media=media).exists()
        else:
            unlock_type = MediaUnlockEnum.UNLOCK_LOCKED
            is_liked = False

        if unlock_type.is_locked():
            wrapped_master_key_for_client = b'x'
            wrap_nonce = b'x'
            session_key = b'x'
        else:
            master_key = self._decrypt_wrapped_master_key(media)
            # Random 32 bytes
            session_key = os.urandom(32)
            # standard 12-byte AES-GCM nonce
            wrap_nonce = os.urandom(12)
            wrapped_master_key_for_client = AESGCM(session_key).encrypt(
                nonce=wrap_nonce,
                data=master_key,
                associated_data=None
            )

        return MediaValueObject(
            media=media,
            wrapped_master_key=wrapped_master_key_for_client,
            wrap_nonce=wrap_nonce,
            session_key=session_key,
            unlock_type=unlock_type,
            is_liked=is_liked,
            total_likes=total_likes,
            total_comments=total_comments
        )

    def _decrypt_wrapped_master_key(self, media: Media) -> bytes:
        root_key = bytes.fromhex(settings.MEDIA_ROOT_ENCRYPT_KEY)
        aesgcm = AESGCM(root_key)

        return (
            aesgcm.decrypt(
                nonce=media.nonce,
                data=media.master_key,
                associated_data=None
            )
        )
