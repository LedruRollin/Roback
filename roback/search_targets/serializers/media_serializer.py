
from rest_framework.serializers import ModelSerializer
 
from search_targets.models import Media
 

class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
