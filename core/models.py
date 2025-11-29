# core/models.py
from django.utils import timezone
from django.db import models
from django.utils.text import slugify

# ===== пост/новина (як було) =====
class Post(models.Model):
    TYPE_CHOICES = (('news', 'Новина'), ('post', 'Стаття'))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self): return self.title
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    @property
    def cover(self):
        return self.images.order_by('order', 'id').first()


def post_image_path(instance, filename):
    return f"posts/{instance.post_id}/{filename}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=post_image_path)
    alt = models.CharField("Опис (alt)", max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    # ручна ширина (використовуємо у статтях)
    width_percent = models.PositiveSmallIntegerField("Ширина (%)", default=50)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image #{self.id} for {self.post.title}"


# ===== КВІЗИ =====
def quiz_upload(instance, filename):
    return f"quiz/{instance.quiz_id}/{filename}"

class Quiz(models.Model):
    title = models.CharField('Назва', max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    subtitle = models.CharField('Підзаголовок', max_length=300, blank=True)
    image_url = models.URLField('Зображення (URL)', blank=True)

    is_active = models.BooleanField('Показувати на сайті', default=True)
    shuffle_questions = models.BooleanField('Міксувати питання', default=False)
    shuffle_answers = models.BooleanField('Міксувати відповіді', default=False)

    # щоб не питало про дефолт при міграції на існуючих рядках:
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Квіз'
        verbose_name_plural = 'Квізи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, verbose_name='Квіз')
    text = models.CharField('Питання', max_length=300)
    image = models.ImageField('Зображення відповіді/питання', upload_to='quiz/q/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'

    def __str__(self):
        return self.text


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='answers', on_delete=models.CASCADE, verbose_name='Питання')
    text = models.CharField('Відповідь', max_length=300, blank=True)
    image = models.ImageField('Зображення відповіді', upload_to='quiz/a/', blank=True, null=True)

    # Для “типологічних” квізів (A/B/C/…)
    code = models.CharField('Код (A/B/C/…)', max_length=5, blank=True)

    # Для тестів з правильною відповіддю
    is_correct = models.BooleanField('Правильна', default=False)

    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'

    def __str__(self):
        return self.text or f'Відповідь #{self.pk}'


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='results', on_delete=models.CASCADE, verbose_name='Квіз')
    code = models.CharField('Код (A/B/C/…)', max_length=5, db_index=True)
    title = models.CharField('Заголовок', max_length=200)
    image = models.ImageField('Зображення результату', upload_to='quiz/r/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Результат'
        verbose_name_plural = 'Результати'

    def __str__(self):
        return f'{self.quiz.title}: {self.code}'


class Horoscope(models.Model):
    sign = models.CharField(max_length=50, verbose_name='Знак')
    date_range = models.CharField(max_length=50, verbose_name='Діапазон дат')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис')

    def __str__(self):
        return f"{self.sign} ({self.date_range})"

# --- Winx cards for homepage ---
from django.utils.text import slugify

class WinxCard(models.Model):
    name = models.CharField('Імʼя', max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    # Кольори з інлайном у шаблоні
    bg_color = models.CharField('Колір фону', max_length=20, default='#e96005',
                                help_text='CSS колір: #hex або rgb/rgba')
    badge_color = models.CharField('Колір бейджа', max_length=20, blank=True,
                                   help_text='Порожньо = як фон')

    # Шари (усе піде в MEDIA)
    wings = models.ImageField('Крила', upload_to='core/winx/')
    body  = models.ImageField('Тіло',  upload_to='core/winx/')
    frame = models.ImageField('Рамка', upload_to='core/winx/')

    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)
    is_active = models.BooleanField('Показувати', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Winx картка'
        verbose_name_plural = 'Winx картки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:120]
        super().save(*args, **kwargs)

    @property
    def effective_badge_color(self):
        return self.badge_color or self.bg_color


# ===== ОПИТУВАННЯ =====
from django.db import models
from django.utils.text import slugify

class Poll(models.Model):
    question   = models.CharField('Питання', max_length=255)
    slug       = models.SlugField(max_length=220, unique=True, blank=True)
    image      = models.ImageField('Зображення', upload_to='polls/', blank=True, null=True)
    is_active  = models.BooleanField('Показувати на сайті', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Опитування'
        verbose_name_plural = 'Опитування'

    def __str__(self): return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)[:220]
        # гарантуємо, що активним буде лише одне опитування
        super().save(*args, **kwargs)
        if self.is_active:
            Poll.objects.exclude(pk=self.pk).update(is_active=False)

    @property
    def total_votes(self):
        return sum(self.options.values_list('votes', flat=True))


class PollOption(models.Model):
    poll   = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text   = models.CharField('Варіант', max_length=200)
    order  = models.PositiveIntegerField('Порядок', default=0, db_index=True)
    votes  = models.PositiveIntegerField('Голосів', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Варіант'
        verbose_name_plural = 'Варіанти'

    def __str__(self): return self.text


# core/models.py
from django.db import models
from django.utils import timezone

class AdBanner(models.Model):
    POSITIONS = [('top', 'Над шапкою')]

    title = models.CharField('Назва', max_length=200)
    position = models.CharField('Позиція', max_length=20, choices=POSITIONS, default='top', db_index=True)
    image = models.ImageField('Зображення', upload_to='ads/')
    alt = models.CharField('ALT-текст', max_length=200, blank=True)
    link_url = models.URLField('Посилання', blank=True)
    open_new_tab = models.BooleanField('Відкривати у новій вкладці', default=True)

    is_active = models.BooleanField('Активний', default=True)
    start_at = models.DateTimeField('Почати показ', blank=True, null=True)
    end_at   = models.DateTimeField('Завершити показ', blank=True, null=True)
    weight   = models.PositiveIntegerField('Вага (пріоритет)', default=1, help_text='Більше = частіше показ')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-weight', '-created_at']
        verbose_name = 'Рекламний банер'
        verbose_name_plural = 'Рекламні банери'

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_at and self.start_at > now:
            return False
        if self.end_at and self.end_at < now:
            return False
        return True




# core/models.py
from django.conf import settings

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='post_comments')
    display_name = models.CharField('Імʼя (якщо не увійшли)', max_length=80, blank=True)
    body = models.TextField('Повідомлення')
    is_public = models.BooleanField('Публічний', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        who = self.display_name or (self.user and self.user.get_username()) or 'Анонім'
        return f'Коментар {who} до "{self.post.title}"'

    def author_name(self):
        if self.display_name:
            return self.display_name
        if self.user and hasattr(self.user, "profile") and getattr(self.user.profile, "display_name", ""):
            return self.user.profile.display_name
        return self.user.get_username() if self.user else "Анонім"
