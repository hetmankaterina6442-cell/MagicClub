from django.db import models
from django.urls import reverse
from django.utils.text import slugify

ENGINE_CHOICES = [('ruffle', 'Ruffle (Flash)')]

class GameTheme(models.Model):
    title = models.CharField('Назва тематики', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField('Опис', blank=True)
    icon = models.ImageField('Іконка', upload_to='games/theme_icons/', blank=True, null=True)
    cover = models.ImageField('Обкладинка', upload_to='games/theme_covers/', blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Тематика ігор'
        verbose_name_plural = 'Тематики ігор'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GameCategory(models.Model):
    # НОВЕ: прив’язка до тематики
    theme = models.ForeignKey(
        GameTheme, on_delete=models.PROTECT, related_name='categories',
        verbose_name='Тематика', blank=True, null=True  # тимчасово null=True для м’якої міграції
    )
    title = models.CharField('Назва категорії', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    icon = models.ImageField('Іконка', upload_to='games/cat_icons/', blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Категорія ігор'
        verbose_name_plural = 'Категорії ігор'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Game(models.Model):
    category = models.ForeignKey(
        GameCategory, on_delete=models.PROTECT, related_name='games',
        verbose_name='Категорія', default=None, blank=True, null=True
    )
    title = models.CharField('Назва', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField('Опис', blank=True)
    engine = models.CharField('Двигун', max_length=20, choices=ENGINE_CHOICES, default='ruffle')
    swf_file = models.FileField('SWF файл', upload_to='games/swf/')
    cover = models.ImageField('Обкладинка', upload_to='games/covers/', blank=True, null=True)
    width = models.PositiveIntegerField('Ширина', default=800)
    height = models.PositiveIntegerField('Висота', default=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Гра'
        verbose_name_plural = 'Ігри'
        indexes = [models.Index(fields=['slug'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("games:game_detail", args=[self.slug])

    def __str__(self):
        return self.title
