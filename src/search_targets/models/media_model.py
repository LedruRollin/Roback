import uuid

from django.db.models import (
    CASCADE,
    FileField,
    ForeignKey,
    Model,
    TextChoices,
    TextField,
)

from search_targets.models import SearchTarget


class MediaType(TextChoices):
    GIF = "GIF"
    Image = "IMAGE"
    Video = "VIDEO"


def get_media_path(instance, _):
    """ Return path in filesystem storage """
    if instance.type == MediaType.Image:
        extension = "png"
    elif instance.type == MediaType.Video:
        extension = "mp4"
    elif instance.type == MediaType.GIF:
        extension = "gif"
    else:
        raise ValueError(f"Unexpected media type {instance.type}")

    return f"{instance.search_target.id}/{uuid.uuid4()}.{extension}"


class Media(Model):
    """ Model for a media (image, video, gif, etc)"""
    search_target = ForeignKey(SearchTarget, on_delete=CASCADE, related_name="media")
    name = TextField()
    file = FileField(upload_to=get_media_path)
    type = TextField(choices=MediaType.choices, default='')
