
from django.forms import ModelForm

from search_targets.models import Media


class MediaForm(ModelForm):
   class Meta:
      model = Media
      fields = "__all__"
