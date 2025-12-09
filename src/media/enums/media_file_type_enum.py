from enum import Enum


class MediaFileTypeEnum(Enum):
    FILE_TYPE_AUDIO = 'audio'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_IMAGE = 'image'

    @staticmethod
    def file_types() -> tuple:
        return (
            (MediaFileTypeEnum.FILE_TYPE_AUDIO.value, 'Audio'),
            (MediaFileTypeEnum.FILE_TYPE_VIDEO.value, 'Video'),
            (MediaFileTypeEnum.FILE_TYPE_IMAGE.value, 'Image'),
        )
