
from django import forms

from firstapp.models import Media, SearchTarget


class SearchTargetForm(forms.ModelForm):
   class Meta:
      model = SearchTarget
      fields = "__all__"


class MediaForm(forms.ModelForm):
   class Meta:
      model = Media
      fields = "__all__"
