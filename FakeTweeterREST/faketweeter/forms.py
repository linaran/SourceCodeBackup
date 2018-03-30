from django import forms
from django.contrib.auth.models import User

from .models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['tweet']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
