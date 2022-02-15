from django import forms
from django.contrib.auth.models import User
from .models import Comments


class CommentForm(forms.ModelForm):
    """Форма отзыва"""

    class Meta:
        model = Comments
        fields = ('name', 'text',)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "id": "contactcomment"})
        }
