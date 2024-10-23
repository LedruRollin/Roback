
from rest_framework.serializers import ModelSerializer, FilePathField, SerializerMethodField
 
from search_targets.models import Media
 

class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "name",
            "file_path",
            "type",
        )
