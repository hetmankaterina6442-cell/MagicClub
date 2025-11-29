from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UAAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Ім’я феї",
        widget=forms.TextInput(attrs={"placeholder": "Ім’я феї"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )

class UASignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Ім’я феї"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Підтвердіть пароль"