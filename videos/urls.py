from django.urls import path
from . import views

app_name = 'videos'
urlpatterns = [
    path('', views.category_list, name='categories'),
    path('c/<slug:slug>/', views.category_detail, name='category'),
    path('v/<slug:slug>/', views.video_detail, name='detail'),
]
