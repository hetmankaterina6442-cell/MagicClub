from django.db import models
from django.utils.text import slugify

class GalleryCategory(models.Model):
    title = models.CharField('Назва категорії', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    icon = models.ImageField('Іконка', upload_to='gallery/cat_icons/', blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Категорія галереї'
        verbose_name_plural = 'Категорії галереї'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Album(models.Model):
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.PROTECT, related_name='albums',
        verbose_name='Категорія', default=None, blank=True, null=True
    )
    title = models.CharField('Назва альбому', max_length=200)
    description = models.TextField('Опис', blank=True)

    # НОВЕ: обкладинка альбому
    cover = models.ImageField('Обкладинка', upload_to='gallery/album_covers/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбоми'

    def __str__(self):
        return self.title

    # URL обкладинки з fallback на перше фото
    def get_cover_url(self):
        if self.cover:
            try:
                return self.cover.url
            except Exception:
                pass
        first = self.photos.order_by('position', 'id').first()
        return first.image.url if first else ''


class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos',
                              on_delete=models.CASCADE, verbose_name='Альбом')
    image = models.ImageField('Фото', upload_to='gallery/photos/')
    caption = models.CharField('Підпис', max_length=220, blank=True)

    # НОВЕ: керування порядком
    position = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'id']   # спершу корист. порядок, далі стабільність
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return self.caption or f"Фото #{self.pk}"
