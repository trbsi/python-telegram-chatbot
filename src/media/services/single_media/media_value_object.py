from protectapp import settings
from src.media.enums.media_unlock_enum import MediaUnlockEnum
from src.media.models import Media


class MediaValueObject:
    def __init__(
            self,
            media: Media,
            wrapped_master_key: bytes,
            wrap_nonce: bytes,
            session_key: bytes,
            unlock_type: MediaUnlockEnum,
            is_liked: bool,
            total_likes: int,
            total_comments: int,
    ):
        self.media = media
        self.wrapped_master_key = wrapped_master_key
        self.wrap_nonce = wrap_nonce
        self.session_key = session_key
        self.unlock_type = unlock_type
        self.is_liked = is_liked
        self.total_likes = total_likes
        self.total_comments = total_comments

    def get_wrapped_master_key(self) -> str:
        return self.wrapped_master_key.hex()

    def get_wrap_nonce(self) -> str:
        return self.wrap_nonce.hex()

    def get_session_key(self) -> str:
        return self.session_key.hex()

    def is_unlocked(self) -> bool:
        return self.unlock_type.is_unlocked_permanent()

    def is_unlock_pending(self) -> bool:
        return self.unlock_type.is_pending()

    def get_video_metadata_as_json(self) -> dict:
        shards = self.media.shards_metadata
        metadata = {
            'total_time_in_seconds': self.media.get_total_time_in_seconds(),
            'codec': self.media.get_codec_string(),
            'seconds_per_shard': self.media.get_seconds_per_shard()
        }

        shard_metadata = []
        for index, shard in enumerate(shards):
            shard_path = self.media.get_shard_file_path(index)
            shard_metadata.append({
                'url': f'{settings.STORAGE_CDN_URL}/{shard_path}',
                'name': self.media.get_shard_name(index),
                'nonce': self.media.get_shard_nonce(index),  # in hex
            })

        metadata['shards'] = shard_metadata
        return metadata
