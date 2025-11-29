# profiles/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_on_signup(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_migrate)
def backfill_profiles(sender, **kwargs):
    # створюємо профілі для старих користувачів, якщо відсутні
    if sender.name.endswith("profiles"):
        for u in User.objects.all():
            Profile.objects.get_or_create(user=u)
