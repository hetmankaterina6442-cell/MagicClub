# core/admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Post, PostImage, Horoscope, WinxCard,
    Quiz, QuizQuestion, QuizAnswer, QuizResult,
)

# ---------- POST & IMAGES ----------

class PostImageInlineForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = "__all__"
        widgets = {
            # слайдер ширини у %
            "width_percent": forms.NumberInput(attrs={
                "type": "range", "min": "20", "max": "100", "step": "5",
                "oninput": 'this.parentElement.querySelector(".wp-val").innerText = this.value + "%";'
            })
        }

class PostImageInline(admin.TabularInline):
    model = PostImage
    form = PostImageInlineForm
    extra = 0
    ordering = ("order", "id")
    fields = ("preview", "image", "alt", "order", "width_percent", "width_display")
    readonly_fields = ("preview", "width_display")

    def preview(self, obj):
        if obj and getattr(obj, "image", None):
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;border:1px solid #eee;"/>',
                obj.image.url
            )
        return "—"

    def width_display(self, obj):
        val = getattr(obj, "width_percent", 50) or 50
        return format_html('<strong class="wp-val">{}</strong>', f"{val}%")
    width_display.short_description = "Поточна ширина"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("title", "slug", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostImageInline]


# ---------- HOROSCOPE ----------

@admin.register(Horoscope)
class HoroscopeAdmin(admin.ModelAdmin):
    list_display = ("sign", "title")


# ---------- QUIZ ----------

class QuizResultInline(admin.TabularInline):
    model = QuizResult
    extra = 0
    ordering = ("order", "id")

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    fields = ("text", "image", "order")
    extra = 1
    ordering = ("order", "id")
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "shuffle_questions", "shuffle_answers")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [QuizResultInline, QuizQuestionInline]


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    fields = ("text", "image", "code", "is_correct", "order")
    extra = 2
    ordering = ("order", "id")

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "order")
    list_filter = ("quiz",)
    ordering = ("quiz", "order", "id")
    inlines = [QuizAnswerInline]

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "code", "is_correct", "order")
    list_filter = ("question__quiz", "is_correct")
    search_fields = ("text",)
    ordering = ("question__quiz", "question__order", "order", "id")

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("quiz", "code", "title", "order")
    list_filter = ("quiz",)
    search_fields = ("title", "code")
    ordering = ("quiz", "order", "id")


# ---------- WINX CARDS ----------

@admin.register(WinxCard)
class WinxCardAdmin(admin.ModelAdmin):
    list_display = ("preview", "name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "slug")
    fields = (
        "name", "slug",
        ("bg_color", "badge_color"),
        ("wings", "body", "frame"),
        "order", "is_active",
        "preview",
    )
    readonly_fields = ("preview",)

    def preview(self, obj):
        if not getattr(obj, "pk", None):
            return "—"
        color = obj.bg_color or "#eee"
        return format_html(
            '<div style="display:flex;gap:8px;align-items:center">'
            '<span style="display:inline-block;width:18px;height:18px;'
            'border-radius:4px;background:{};border:1px solid #ddd"></span>'
            '{}'
            '</div>',
            color, obj.name
        )
    preview.short_description = "Перегляд"


from .models import Poll, PollOption

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2
    fields = ('text', 'order', 'votes')
    readonly_fields = ('votes',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'total_votes', 'created_at')
    list_filter  = ('is_active',)
    prepopulated_fields = {'slug': ('question',)}
    inlines = [PollOptionInline]


# core/admin.py  (додай наприкінці файлу)
from django.contrib import admin
from django.utils.html import format_html
from .models import AdBanner

@admin.register(AdBanner)
class AdBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active', 'start_at', 'end_at', 'weight', 'preview')
    list_filter  = ('position', 'is_active')
    search_fields = ('title', 'link_url')
    ordering = ('-weight', '-created_at')
    fields = (
        'title', ('position','is_active','weight'),
        ('start_at','end_at'),
        ('image','alt'),
        ('link_url','open_new_tab'),
        'preview',
    )
    readonly_fields = ('preview',)

    def preview(self, obj):
        if not obj or not obj.image:
            return '—'
        return format_html(
            '<div style="max-width:720px;border:1px solid #eee;border-radius:8px;overflow:hidden">'
            '<img src="{}" style="width:100%;display:block;"></div>', obj.image.url
        )
    preview.short_description = 'Передперегляд'


# core/admin.py
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author_name', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'post__type')
    search_fields = ('display_name', 'body', 'post__title', 'user__username')
