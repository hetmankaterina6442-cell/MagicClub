from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.theme_list, name='theme_list'),

    # коротка адреса гри
    path('g/<slug:slug>/', views.game_detail, name='game_detail'),
    path('play/<slug:slug>/', views.game_play, name='play'),

    # теми/категорії
    path('<slug:theme_slug>/', views.theme_detail, name='theme_detail'),
    path('<slug:theme_slug>/<slug:category_slug>/', views.category_detail, name='category_detail'),

    # вкладений шлях до гри (рідше використовуємо)
    path('<slug:theme_slug>/<slug:category_slug>/<slug:slug>/',
         views.game_detail, name='game_detail_nested'),
]
