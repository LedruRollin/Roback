import uuid

from django.conf import settings
from django.db.models import CASCADE
from django.db.models import FileField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import TextChoices
from django.db.models.fields import TextField

from search_targets.models import SearchTarget


class MediaType(TextChoices):
    GIF = "GIF"
    Image = "IMAGE"
    Video = "VIDEO"


def get_media_path(instance, _):
    """ Return path in filesystem storage """
    extension = "file"
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


    def save(self, *args, **kwargs):
        # Set media type
        content_type = self.file.file.content_type
        if content_type not in settings.ACCEPTED_MIME_TYPES:
            raise ValueError(f"Unsupported media type {content_type}")
        media_type = settings.ACCEPTED_MIME_TYPES[content_type]
        self.type = MediaType(media_type)
        super().save(*args, **kwargs)

