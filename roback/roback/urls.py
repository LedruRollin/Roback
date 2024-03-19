"""
URL configuration for roback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from firstapp import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register("search_targets", views.SearchTargetAPIView, basename="search_targets")
router.register("medias", views.MediaAPIView, basename="medias")


urlpatterns = [
    path('admin/', admin.site.urls),
#     path('liste/', views.hello),
#     path('liste/<int:search_target_id>/', views.search_target_unique, name="search-target-unique"),
#     path('liste/<int:search_target_id>/edit', views.edit_search_target, name="edit-search-target"),
#     path('liste-add/', views.add_search_target, name="add-search-target"),
#     path('target-created/', views.search_target_created, name="target-created"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
