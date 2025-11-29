# profiles/views.py
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import RegistrationForm, ProfileForm
from .models import Profile
# profiles/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def fast_logout(request):
    """Миттєвий logout без підтвердження."""
    logout(request)
    next_url = request.GET.get("next") or request.POST.get("next") or "/"
    return redirect(next_url)





def register(request):
    if request.user.is_authenticated:
        return redirect("profiles:me")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Ласкаво просимо! Профіль створено."))
            return redirect("profiles:edit")
    else:
        form = RegistrationForm()
    return render(request, "profiles/register.html", {"form": form})

@login_required
def me(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "profiles/me.html", {"profile": profile})

@login_required
def edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Зміни збережено."))
            return redirect("profiles:me")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles/edit.html", {"form": form})
