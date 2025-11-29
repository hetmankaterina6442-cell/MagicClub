from django.db import migrations

def set_positions(apps, schema_editor):
    Photo = apps.get_model('gallery', 'Photo')
    Album = apps.get_model('gallery', 'Album')

    for album in Album.objects.all():
        qs = Photo.objects.filter(album=album).order_by('created_at', 'id')
        pos = 1
        batch = []
        for p in qs:
            p.position = pos
            pos += 1
            batch.append(p)
            if len(batch) >= 500:
                Photo.objects.bulk_update(batch, ['position'])
                batch = []
        if batch:
            Photo.objects.bulk_update(batch, ['position'])

class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_fill_photo_positions'),  # <- автоматично підставиться django
    ]

    operations = [
        migrations.RunPython(set_positions, migrations.RunPython.noop),
    ]
