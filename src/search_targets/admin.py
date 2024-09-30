from django.contrib import admin

from search_targets.models import Media, SearchTarget, URL


class SearchTargetAdmin(admin.ModelAdmin):
    list_display = ("search_text", "insertion_date", "insertion_time")

class MediaAdmin(admin.ModelAdmin):
    list_display = ("search_target", "type", "file", "name")

class URLAdmin(admin.ModelAdmin):
    list_display = ("url",)

admin.site.register(SearchTarget, SearchTargetAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(URL, URLAdmin)

