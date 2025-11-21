import uuid

from src.media.models import Media


def remote_file_path_for_media(media: Media, extension: str, type: str) -> str:
    extension = extension.replace('.', '')
    file_name = f'{media.__class__.__name__}_{media.id}_{type}_{uuid.uuid4()}.{extension}'
    return f'{media.file_type}/media/{media.user_id}/{file_name}'
