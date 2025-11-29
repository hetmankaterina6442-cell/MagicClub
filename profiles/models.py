# profiles/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

def avatar_path(instance, filename):
    return f"profiles/avatars/{instance.user_id}/{filename}"

class Profile(models.Model):
    FEMALE = "f"
    MALE = "m"
    OTHER = "o"
    GENDER_CHOICES = [
        (FEMALE, "Жінка"),
        (MALE, "Чоловік"),
        (OTHER, "Інше"),
    ]

    AGE_CHOICES = [
        ("under13", "До 13"),
        ("13-17", "13–17"),
        ("18+", "18+"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="profile")
    display_name = models.CharField("Прізвисько", max_length=50, blank=True)
    country = models.CharField("Країна", max_length=80, blank=True)
    gender = models.CharField("Стать", max_length=1, choices=GENDER_CHOICES, blank=True)
    age_group = models.CharField("Вік", max_length=10, choices=AGE_CHOICES, blank=True)
    birth_date = models.DateField("День народження", blank=True, null=True)

    avatar = models.ImageField("Аватар", upload_to=avatar_path, blank=True, null=True)
    bio = models.TextField("Про себе", blank=True)

    newsletter_opt_in = models.BooleanField("Отримувати новини", default=False)
    terms_accepted_at = models.DateTimeField("Погоджено з умовами", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        return self.display_name or self.user.get_username()
