from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-custom'
    }))
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-custom'
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control form-custom'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-custom'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class ReviewForm(forms.ModelForm):
    content = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={
        "class": "form-control form-custom",
        "rows": 5
    }))

    class Meta:
        model = Review
        fields = ["content"]
