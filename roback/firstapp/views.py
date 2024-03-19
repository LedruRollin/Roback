
import re

from django.forms import modelformset_factory
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser

from firstapp.models import SearchTarget
from firstapp.models import SearchTarget, Media, URL
from firstapp.formulaire import SearchTargetForm, MediaForm
from firstapp.paginations import PaginationWithTotalCount
from firstapp.serializers import SearchTargetSerializer, MediaSerializer

from typing import List


def hello(request):
    search_targets = SearchTarget.objects.all()
    print("hello")
    return render(
        request, 
        "firstapp/search_target_list.html",
        {"search_targets": search_targets}    
    )

def search_target_unique(request, search_target_id):
    search_target = SearchTarget.objects.get(id=search_target_id)
    print("search_target_unique")
    return render(
        request, 
        "firstapp/search_target_unique.html",
        {"search_target": search_target}    
    )


def add_search_target(request):

    if request.method == 'GET':
        # ceci doit être une requête GET, donc créer un formulaire vide
        print("GET add_search_target")
        form = SearchTargetForm()
    elif request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        print("POST add_search_target")
        form = SearchTargetForm(request.POST, files=request.FILES)
        if form.is_valid():
            search_target = form.save()
            return redirect('search-target-unique', search_target.id)
    else:
        raise ValueError(f"Unexpected request method {request.method}")

    return render(request,
            'firstapp/add_search_target.html',
            {'form': form})  # passe ce formulaire au gabarit


def search_target_created(request):
    print("search_target_created")
    return render(request, 
                    'firstapp/search_target_created.html',
                    # {"search_target": search_target}
                )

def edit_search_target(request, search_target_id):

    if request.method == 'GET':
        print("GET edit_search_target")
        # Formulaire rempli à partir de l'objet existant
        search_target = SearchTarget.objects.get(id=search_target_id)
        form = SearchTargetForm(instance=search_target)
    elif request.method == 'POST':
        print("POST edit_search_target")
        search_target = SearchTarget.objects.get(id=search_target_id)
        form = SearchTargetForm(request.POST, files=request.FILES, instance=search_target)
        if form.is_valid():
            search_target = form.save()
            return redirect('search-target-unique', search_target.id)
    else:
        raise ValueError(f"Unexpected request method {request.method}")

    return render(
        request, 
        "firstapp/edit_search_target.html",
        {"form": form}    
    )


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
        # Retrieving
        queryset = SearchTarget.objects.all()

        # Filtering
        search_text = self.request.GET.get("search")
        if search_text is not None:
           queryset = queryset.filter(search_text__icontains=search_text)

        queryset = queryset.order_by("insertion_date")
        return queryset

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            search_target_form = SearchTargetForm(request.POST)

            if search_target_form.is_valid():
                search_target = search_target_form.save()

                text = search_target.search_text
                urls = extract_url_from_text(text)
                for url in urls:
                    url = URL(
                        search_target=search_target,
                        url=url
                    )
                    url.save()

                my_post_dict = request.POST.copy()
                my_post_dict['form-TOTAL_FORMS'] = len(request.FILES)
                my_post_dict['form-INITIAL_FORMS'] = 0
                my_post_dict['form-MAX_NUM_FORMS'] = 1000
                image_formset = self.image_formset(my_post_dict, files=request.FILES)
                if image_formset.is_valid():
                    for media_file_name, media_file in image_formset.files.items():
                        media = Media(
                            search_target=search_target,
                            file=media_file,
                            name=media_file_name,
                        )
                        media.save()

                    return redirect('search-target-unique', search_target.id)
        else:
            return HttpResponseNotAllowed(['POST'])

    def list(self, request, *args, **kwargs):
        print("test")
        return super().list(request, *args, **kwargs)

    def count():
        return SearchTarget.objects.count()


class MediaAPIView(ModelViewSet):

    serializer_class = MediaSerializer

    def get_queryset(self):
        return Media.objects.all()

    def retrieve(self, request, pk):
        queryset = Media.objects.get(pk)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

