
import re

import magic

from django.conf import settings
from django.forms import modelformset_factory
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from search_targets.models import Media, MediaType, SearchTarget, URL
from search_targets.forms import SearchTargetForm, MediaForm
from search_targets.paginations import PaginationWithTotalCount
from search_targets.serializers import SearchTargetSerializer

from typing import List


def extract_url_from_text(text: str) -> List[str]:
    REGEX = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    matches = list(re.finditer(REGEX, text))
    return [match.group(0) for match in matches]


class SearchTargetAPIView(ModelViewSet):

    pagination_class = PaginationWithTotalCount
    serializer_class = SearchTargetSerializer
    parser_classes = [MultiPartParser]
    image_formset = modelformset_factory(Media, form=MediaForm, extra=3)

    def get_queryset(self):
        queryset = SearchTarget.objects.all()

        # Filtering
        search_text = self.request.GET.get("search")
        if search_text is not None:
           queryset = queryset.filter(search_text__icontains=search_text)

        queryset = queryset.order_by("insertion_date")
        return queryset

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            search_target_form = SearchTargetForm(request.POST)

            if not search_target_form.is_valid():
                return JsonResponse({"status": "error", "message": search_target_form.errors}, status=400)
            # Search target save
            search_target = search_target_form.save()

            # URL save
            text = search_target.search_text
            urls = extract_url_from_text(text)
            for url in urls:
                url = URL(
                    search_target=search_target,
                    url=url
                )
                url.save()

            # Media save
            my_post_dict = request.POST.copy()
            my_post_dict['form-TOTAL_FORMS'] = len(request.FILES)
            my_post_dict['form-INITIAL_FORMS'] = 0
            my_post_dict['form-MAX_NUM_FORMS'] = 1000
            image_formset = self.image_formset(my_post_dict, files=request.FILES)
            if image_formset.is_valid():
                for media_file_name, media_file in image_formset.files.items():
                    # Check mime type
                    mime_type = magic.from_buffer(media_file.read(), mime=True)
                    if mime_type not in settings.ACCEPTED_MIME_TYPES:
                        raise ValueError(f"Unsupported media type {mime_type}")
                    media_type = settings.ACCEPTED_MIME_TYPES[mime_type]

                    media = Media(
                        search_target=search_target,
                        file=media_file,
                        name=media_file_name,
                        type=MediaType(media_type)
                    )

                    media.save()

            serializer = self.serializer_class(search_target)
            return Response(serializer.data)
        else:
            return HttpResponseNotAllowed(['POST'])

    @staticmethod
    def count():
        return SearchTarget.objects.count()
