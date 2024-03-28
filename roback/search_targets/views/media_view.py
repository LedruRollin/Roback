
from rest_framework.viewsets import ModelViewSet

from search_targets.models import Media
from search_targets.serializers import MediaSerializer


class MediaAPIView(ModelViewSet):

    serializer_class = MediaSerializer

    def get_queryset(self):
        return Media.objects.all()

    def retrieve(self, request, pk):
        queryset = Media.objects.get(pk)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
