# core/context_processors.py
import random
from django.db.models import Q
from django.utils import timezone
from .models import AdBanner

def site_banners(request):
    now = timezone.now()
    qs = AdBanner.objects.filter(
        position='top', is_active=True
    ).filter(
        Q(start_at__isnull=True) | Q(start_at__lte=now)
    ).filter(
        Q(end_at__isnull=True) | Q(end_at__gte=now)
    )

    top_banner = None
    items = list(qs)
    if items:
        weights = [max(1, b.weight) for b in items]
        top_banner = random.choices(items, weights=weights, k=1)[0]

    return {'top_banner': top_banner}
