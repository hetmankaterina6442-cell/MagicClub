# core/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("display_name", "body")
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Ваш нік"}),
            "body": forms.Textarea(attrs={"placeholder": "Ваш коментар"}),
        }
