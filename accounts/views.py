from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UAAuthenticationForm, UASignUpForm

class FairyLoginView(LoginView):
    template_name = "accounts/login_panel.html"
    authentication_form = UAAuthenticationForm
    redirect_authenticated_user = True

class SignUpView(CreateView):
    model = User
    form_class = UASignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")