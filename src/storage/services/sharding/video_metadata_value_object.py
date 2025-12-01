from src.storage.services.sharding.shard_metadata_value_object import ShardMetadataValueObject


class VideoMetadataValueObject:
    def __init__(
            self,
            shards_metadata: list[ShardMetadataValueObject],
            video_duration_in_seconds: float,
    ):
        self.shards_metadata = shards_metadata
        self.video_duration_in_seconds = video_duration_in_seconds
