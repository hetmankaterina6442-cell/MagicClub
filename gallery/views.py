from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, Album

def album_list(request, category_slug=None):
    categories = GalleryCategory.objects.all()
    albums = Album.objects.select_related('category').prefetch_related('photos')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(GalleryCategory, slug=category_slug)
        albums = albums.filter(category=active_category)
    return render(request, 'gallery/album_list.html', {
        'categories': categories,
        'albums': albums,
        'active_category': active_category
    })

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()  # вже відсортовано Meta.ordering (position, id)
    return render(request, 'gallery/album_detail.html', {
        'album': album,
        'photos': photos
    })
