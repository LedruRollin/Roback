from django.forms import ModelForm

from search_targets.models import SearchTarget


class SearchTargetForm(ModelForm):
   class Meta:
      model = SearchTarget
      fields = "__all__"
