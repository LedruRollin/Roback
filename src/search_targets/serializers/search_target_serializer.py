
from rest_framework.serializers import ModelSerializer
 
from search_targets.models import SearchTarget


class SearchTargetSerializer(ModelSerializer):

    class Meta:
        model = SearchTarget
        fields = [
            "id", 
            "search_text", 
            "insertion_date",
            "insertion_time",
            "origin",
            "original_url",
            "media"
        ]


