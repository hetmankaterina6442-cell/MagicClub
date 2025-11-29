# profiles/urls.py
from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("me/", views.me, name="me"),
    path("me/edit/", views.edit, name="edit"),
    path("logout/", views.fast_logout, name="logout"),
]
