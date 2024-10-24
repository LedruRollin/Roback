
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from search_targets.models import Media
from search_targets.serializers import MediaSerializer


class MediaAPIView(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = MediaSerializer

    def get_queryset(self):
        queryset = Media.objects.all()
        queryset = queryset.order_by("search_target")
        return queryset
