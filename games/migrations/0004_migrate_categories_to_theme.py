from django.db import migrations

def forwards(apps, schema_editor):
    GameTheme = apps.get_model('games', 'GameTheme')
    GameCategory = apps.get_model('games', 'GameCategory')

    # створюємо тематику Winx (якщо ще немає)
    winx, _ = GameTheme.objects.get_or_create(
        slug='winx',
        defaults={'title': 'Winx', 'description': 'Усі ігри з всесвіту Winx'}
    )

    # проставляємо тематику всім наявним категоріям
    GameCategory.objects.filter(theme__isnull=True).update(theme=winx)

def backwards(apps, schema_editor):
    # у зворотному напрямку просто не знімаємо значення
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_gametheme_gamecategory_theme'),  # ← попередня згенерована міграція
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
