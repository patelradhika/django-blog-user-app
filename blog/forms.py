from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    check_password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Column('username', css_class="px-5"),
        Column('email', css_class="mt-2 px-5"),
        Column('password', css_class="mt-2 px-5"),
        Column('check_password', css_class="mt-2 px-5"),
        Column(Submit('submit', 'Register', css_class="col-2 btn btn-primary"), css_class="mt-2 px-5")
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Column('username', css_class="px-5"),
        Column('password', css_class="mt-2 px-5"),
        Column(Submit('submit', 'Log In', css_class="col-2 btn btn-primary"), css_class="mt-4 px-5")
    )