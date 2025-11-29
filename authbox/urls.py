from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import login_view, signup_view, ForgotPasswordView

app_name = "authbox"

urlpatterns = [
    path("login/",  login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", signup_view, name="signup"),

    path("forgot/", ForgotPasswordView.as_view(), name="forgot"),
    path("forgot/done/", PasswordResetDoneView.as_view(template_name="authbox/forgot_done.html"), name="forgot_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="authbox/reset_confirm.html"), name="password_reset_confirm"),
    path("reset/complete/", PasswordResetCompleteView.as_view(template_name="authbox/reset_complete.html"), name="password_reset_complete"),
]
