# profiles/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.utils import timezone

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Електронна пошта", required=True)
    display_name = forms.CharField(label="Прізвисько", max_length=50)
    country = forms.CharField(label="Країна", required=False)
    gender = forms.ChoiceField(label="Стать", choices=Profile.GENDER_CHOICES, required=False)
    age_group = forms.ChoiceField(label="Вік", choices=Profile.AGE_CHOICES)
    birth_date = forms.DateField(label="День народження", required=False,
                                 widget=forms.DateInput(attrs={"type": "date"}))
    newsletter_opt_in = forms.BooleanField(label="Хочу отримувати новини", required=False)
    accept_terms = forms.BooleanField(label="Я погоджуюся з цими умовами", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2",
                  "display_name", "country", "gender", "age_group",
                  "birth_date", "newsletter_opt_in", "accept_terms")

        # гарні базові стилі поля
        widgets = {
            "username": forms.TextInput(attrs={"class": "reg-input"}),
            "email": forms.EmailInput(attrs={"class": "reg-input"}),
            "password1": forms.PasswordInput(attrs={"class": "reg-input"}),
            "password2": forms.PasswordInput(attrs={"class": "reg-input"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # створюємо або оновлюємо профіль
            prof, _ = Profile.objects.get_or_create(user=user)
            prof.display_name = self.cleaned_data["display_name"]
            prof.country = self.cleaned_data.get("country", "")
            prof.gender = self.cleaned_data.get("gender", "")
            prof.age_group = self.cleaned_data.get("age_group", "")
            prof.birth_date = self.cleaned_data.get("birth_date")
            prof.newsletter_opt_in = self.cleaned_data.get("newsletter_opt_in", False)
            prof.terms_accepted_at = timezone.now()
            prof.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("display_name", "country", "gender", "age_group",
                  "birth_date", "avatar", "bio", "newsletter_opt_in")
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "reg-input"}),
            "country": forms.TextInput(attrs={"class": "reg-input"}),
            "bio": forms.Textarea(attrs={"rows": 4, "class": "reg-input"}),
        }
