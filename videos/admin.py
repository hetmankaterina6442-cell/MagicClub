# videos/admin.py
from django.contrib import admin
from .models import Video, VideoCategory

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

class SourceFilter(admin.SimpleListFilter):
    title = "Джерело"
    parameter_name = "src"

    def lookups(self, request, model_admin):
        return (
            ("yt", "YouTube"),
            ("file", "Файл"),
            ("both", "Файл + YouTube"),
            ("empty", "Без джерела"),
        )

    def queryset(self, request, qs):
        v = self.value()
        if v == "yt":
            return qs.exclude(youtube_url__isnull=True).exclude(youtube_url="")
        if v == "file":
            return qs.exclude(file__isnull=True).exclude(file="")
        if v == "both":
            return qs.exclude(youtube_url__isnull=True).exclude(youtube_url="") \
                     .exclude(file__isnull=True).exclude(file="")
        if v == "empty":
            return qs.filter(youtube_url__isnull=True, file__isnull=True)
        return qs

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "category", "created_at")
    search_fields = ("title", "description", "youtube_url", "slug")
    list_filter = (SourceFilter, "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)

    # метод для list_display
    def source(self, obj):
        if obj.youtube_url and obj.file:
            return "YouTube + файл"
        if obj.youtube_url:
            return "YouTube"
        if obj.file:
            return "Файл"
        return "—"
    source.short_description = "Джерело"
