
from django.db.models import Model
from django.db.models import TextChoices
from django.db.models.fields import (
  DateField,
  TextField,
  TimeField,
  URLField,
)


class SearchTarget(Model):
    """ Model for a search target (any text in which search can be performed)"""

    def __str__(self) -> str:
        return f"{self.search_text} ({self.insertion_date})"
    
    class Origin(TextChoices):
        Twitter = "Twitter"

    search_text = TextField()
    insertion_date = DateField(auto_now_add=True)
    insertion_time = TimeField(auto_now_add=True)
    origin = TextField(choices=Origin.choices, blank=True, default='')
    original_url = URLField(blank=True, default='')
