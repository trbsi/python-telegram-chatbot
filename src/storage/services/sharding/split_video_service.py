import json
import os.path
import subprocess
from pathlib import Path

from protectapp import settings
from src.media.models import Media
from src.storage.services.sharding.shard_metadata_value_object import ShardMetadataValueObject
from src.storage.services.sharding.video_metadata_value_object import VideoMetadataValueObject


class SplitVideoService:
    def split_video_by_seconds(
            self,
            media: Media,
            local_file_path: str,
            seconds_per_video: int = 10
    ) -> VideoMetadataValueObject:
        output_dir = os.path.join(settings.MEDIA_ROOT, 'temp', str(media.id))
        input_path = Path(local_file_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get video duration
        video_duration = self._get_video_duration(local_file_path)

        # Example: output_000.mp4, output_001.mp4, ...
        output_pattern = str(output_dir / "shard_%03d.mp4")

        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", str(seconds_per_video),
            "-reset_timestamps", "1",
            "-force_key_frames", f"expr:gte(t,n_forced*{seconds_per_video})",
            output_pattern
        ]

        subprocess.run(cmd, check=True)

        # Collect shards
        shards = sorted(output_dir.glob("shard_*.mp4"))
        number_of_shards = len(shards)

        meta = []
        for idx, shard in enumerate(shards):
            duration = seconds_per_video
            # Because last shard can have smaller duration
            if idx == number_of_shards - 1:
                tmp_duration = video_duration - idx * seconds_per_video
                if tmp_duration > 0:
                    duration = tmp_duration

            meta.append(
                ShardMetadataValueObject(
                    file=shard,
                    start_time=idx * seconds_per_video,
                    duration=duration
                ))

        return VideoMetadataValueObject(
            shards_metadata=meta,
            video_duration_in_seconds=video_duration
        )

    def _get_video_duration(local_file_path: str) -> float:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            local_file_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
