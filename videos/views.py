from django.shortcuts import render, get_object_or_404
from .models import Video, VideoCategory

def category_list(request):
    cats = VideoCategory.objects.all()
    return render(request, 'videos/categories.html', {'cats': cats})

def category_detail(request, slug):
    cat = get_object_or_404(VideoCategory, slug=slug)
    items = cat.videos.all()
    return render(request, 'videos/list.html', {'category': cat, 'items': items})

def video_detail(request, slug):
    item = get_object_or_404(Video, slug=slug)
    return render(request, 'videos/detail.html', {'item': item})
