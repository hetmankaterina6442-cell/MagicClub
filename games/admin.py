from django.contrib import admin
from .models import GameTheme, GameCategory, Game
from django.utils.html import format_html

@admin.register(GameTheme)
class GameThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'cat_count', 'cover_preview')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    def cat_count(self, obj):
        return obj.categories.count()
    cat_count.short_description = 'Категорій'

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="height:34px;border-radius:6px;">', obj.cover.url)
        return '—'
    cover_preview.short_description = 'Обкладинка'


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'slug', 'game_count', 'icon_preview')
    list_filter = ('theme',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('theme',)

    def game_count(self, obj):
        return obj.games.count()
    game_count.short_description = 'Ігор'

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="height:26px;border-radius:6px;">', obj.icon.url)
        return '—'
    icon_preview.short_description = 'Іконка'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_theme', 'category', 'engine', 'created_at')
    list_filter = ('engine', 'category__theme')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('category',)
    list_select_related = ('category', 'category__theme')

    def get_theme(self, obj):
        return obj.category.theme if obj.category else '—'
    get_theme.short_description = 'Тематика'
