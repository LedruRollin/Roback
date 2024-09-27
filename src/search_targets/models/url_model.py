
from django.db.models import Model
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.db.models.fields import URLField

from search_targets.models import SearchTarget


class URL(Model):
    """ Model for an URL """
    search_target = ForeignKey(SearchTarget, on_delete=CASCADE, related_name="search_target_url")
    url = URLField()
