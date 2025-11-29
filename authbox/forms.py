from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginBoxForm(AuthenticationForm):
    username = forms.CharField(
        label="Fairy Name",
        widget=forms.TextInput(attrs={"class": "abox-input"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "abox-input"})
    )


class SignupForm(forms.Form):
    username = forms.CharField(label="Fairy Name", max_length=150)
    email = forms.EmailField(label="Email (optional)", required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password (again)", widget=forms.PasswordInput)

    def clean_username(self):
        u = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError("This Fairy Name is already taken.")
        return u

    def clean(self):
        data = super().clean()
        if data.get("password1") != data.get("password2"):
            self.add_error("password2", "Passwords don’t match.")
        return data

    def create_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data.get("email") or "",
            password=self.cleaned_data["password1"],
        )
