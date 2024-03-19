from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework.serializers import StringRelatedField
from rest_framework.serializers import CharField
 
from firstapp.models import SearchTarget, Media
 

class MediaSerializer(ModelSerializer):
# class MediaSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class SearchTargetSerializer(ModelSerializer):

    media = MediaSerializer(many=True)
 
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


