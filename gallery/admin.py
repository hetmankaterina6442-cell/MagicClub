from django.contrib import admin
from .models import GalleryCategory, Album, Photo
from django.utils.html import format_html

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    fields = ('preview', 'image', 'caption', 'position')
    readonly_fields = ('preview',)
    ordering = ('position',)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;">', obj.image.url)
        return '—'
    preview.short_description = 'Превʼю'

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'photo_count', 'cover_thumb', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    fields = ('category', 'title', 'description', 'cover', 'cover_preview')
    readonly_fields = ('cover_preview',)
    inlines = [PhotoInline]

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Фото'

    def cover_thumb(self, obj):
        url = obj.get_cover_url()
        if url:
            return format_html('<img src="{}" style="height:34px;border-radius:6px;">', url)
        return '—'
    cover_thumb.short_description = 'Обкладинка'

    def cover_preview(self, obj):
        url = obj.get_cover_url()
        if url:
            return format_html('<img src="{}" style="max-height:180px;border-radius:8px;">', url)
        return '—'
    cover_preview.short_description = 'Превʼю'
