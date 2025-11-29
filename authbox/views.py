from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .forms import LoginBoxForm, SignupForm

def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    if request.method == "POST":
        form = LoginBoxForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
    else:
        form = LoginBoxForm(request)
    return render(request, "authbox/login_page.html", {"form": form, "next": next_url})

def signup_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            from django.contrib.auth import authenticate
            auth_user = authenticate(username=user.username, password=form.cleaned_data["password1"])
            if auth_user:
                login(request, auth_user)
            messages.success(request, "Welcome to Winx Club!")
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, "authbox/signup.html", {"form": form, "next": next_url})

class ForgotPasswordView(PasswordResetView):
    template_name = "authbox/forgot.html"
    success_url = reverse_lazy("authbox:forgot_done")
