from django.db import models
from django.conf import settings
import datetime
import uuid


    
class MediaType(models.TextChoices):
    GIF = "GIF"
    Image = "IMAGE"
    Video = "VIDEO"


def get_media_path(instance, filename):
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


class SearchTarget(models.Model):
    """ Model for a search target (any text in which search can be performed)"""

    def __str__(self) -> str:
        return f"{self.search_text} ({self.insertion_date})"
    
    class Origin(models.TextChoices):
        Twitter = "Twitter"

    search_text = models.fields.TextField()
    insertion_date = models.DateField(auto_now_add=True)
    insertion_time = models.TimeField(auto_now=True)
    origin = models.TextField(choices=Origin.choices, blank=True, default='')
    # url = models.URLField(blank=True, default='')
    original_url = models.URLField(blank=True, default='')


class URL(models.Model):
    search_target = models.ForeignKey(SearchTarget, on_delete=models.CASCADE, related_name="search_target_url")
    url = models.URLField()


class Media(models.Model):
    """ Model for a media (image, video, gif, etc)"""

    search_target = models.ForeignKey(SearchTarget, on_delete=models.CASCADE, related_name="media")
    name = models.fields.TextField()
    file = models.FileField(upload_to=get_media_path)
    type = models.TextField(choices=MediaType.choices, default='')


    def save(self, *args, **kwargs):
        # Set media type
        content_type = self.file.file.content_type
        if content_type not in settings.ACCEPTED_MIME_TYPES:
            raise ValueError(f"Unsupported media type {content_type}")
        media_type = settings.ACCEPTED_MIME_TYPES[content_type]
        self.type = MediaType(media_type)
        super().save(*args, **kwargs)


