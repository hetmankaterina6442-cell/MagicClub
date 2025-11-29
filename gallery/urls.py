from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('cat/<slug:category_slug>/', views.album_list, name='album_by_category'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),
]
