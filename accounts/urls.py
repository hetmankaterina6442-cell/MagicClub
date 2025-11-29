from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView
from .views import FairyLoginView, SignUpView

app_name = "accounts"

urlpatterns = [
    path("login/", FairyLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password-reset/", PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="password_reset"),
]