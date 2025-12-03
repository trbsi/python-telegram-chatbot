import uuid

from src.media.models import Media


def remote_file_path_for_media(media: Media, extension: str, type: str) -> str:
    extension = extension.replace('.', '')
    media_class = media.__class__.__name__
    file_name = f'{media_class}_{media.id}_{type}_{uuid.uuid4()}.{extension}'
    return f'{media.file_type}/user/{media.user_id}/media/{media.id}/{file_name}'.lower()


def remote_shard_file_path_for_media(media: Media, shard_name: str) -> str:
    return f'{media.file_type}/user/{media.user_id}/media/{media.id}/shards/{shard_name}'.lower()
