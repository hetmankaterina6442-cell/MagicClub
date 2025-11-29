# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('videos/', include(('videos.urls', 'videos'), namespace='videos')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('gallery/', include(('gallery.urls', 'gallery'), namespace='gallery')),
    path("account/", include(("authbox.urls", "authbox"), namespace="authbox")),
    path("accounts/", include("profiles.urls", namespace="profiles")),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
