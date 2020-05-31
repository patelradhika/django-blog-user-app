from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import UserImage, BlogPost

class UserForm(forms.ModelForm):
    email = forms.EmailField(label="Email ID")
    password = forms.CharField(widget=forms.PasswordInput())
    check_password = forms.CharField(label="Re-enter Password", widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class AccountForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    check_pass = forms.CharField(label="Re-enter Password", widget=forms.PasswordInput(), required=False)
    image = forms.ImageField(label="Upload Profile Pic", required=False)

    class Meta:
        model = UserImage
        fields = ['image',]


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content',]