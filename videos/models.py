from django.db import models
from django.utils.text import slugify
import re

class VideoCategory(models.Model):
    title = models.CharField('Назва категорії', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    icon = models.ImageField('Іконка', upload_to='videos/cat_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Категорія відео'
        verbose_name_plural = 'Категорії відео'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


SOURCE_CHOICES = (
    ('upload', 'Завантажений файл'),
    ('youtube', 'YouTube'),
)

YOUTUBE_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?'
    r'(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)'
    r'([A-Za-z0-9_-]{11})'
)

# videos/models.py
from django.db import models
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs

class Video(models.Model):
    category   = models.ForeignKey('VideoCategory', on_delete=models.PROTECT,
                                   related_name='videos', verbose_name='Категорія',
                                   blank=True, null=True, default=None)
    title      = models.CharField('Назва', max_length=200)
    slug       = models.SlugField(max_length=220, unique=True, blank=True)
    description= models.TextField('Опис', blank=True)

    # NEW
    youtube_url = models.URLField('Посилання на YouTube', blank=True)
    file        = models.FileField('Відеофайл', upload_to='videos/', blank=True, null=True)

    thumbnail   = models.ImageField('Постер', upload_to='videos/thumbs/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['slug'])]
        verbose_name = 'Відео'
        verbose_name_plural = 'Відео'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    # ---- helpers ----
    @property
    def is_youtube(self):
        return bool(self.youtube_url)

    @property
    def youtube_id(self):
        """Повертає чистий ID з будь-якого посилання: watch, youtu.be, shorts, embed."""
        url = (self.youtube_url or "").strip()
        if not url:
            return ""
        p = urlparse(url)

        # youtu.be/<id>
        if 'youtu.be' in p.netloc:
            return p.path.lstrip('/').split('/')[0]

        # youtube.com/shorts/<id>, /embed/<id>
        if p.path.startswith('/shorts/'):
            return p.path.split('/shorts/')[1].split('/')[0]
        if p.path.startswith('/embed/'):
            return p.path.split('/embed/')[1].split('/')[0]

        # youtube.com/watch?v=<id>
        qs = parse_qs(p.query)
        if 'v' in qs:
            return qs['v'][0]

        return ""

    @property
    def player_url(self):
        """URL для iframe/плеєра у лайтбоксі."""
        if self.is_youtube and self.youtube_id:
            # nocookie – менше проблем з куками та блокувальниками
            return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}?rel=0&modestbranding=1"
        return self.file.url if self.file else ""

    @property
    def poster_url(self):
        if self.is_youtube and self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
        return self.thumbnail.url if self.thumbnail else ""
