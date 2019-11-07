from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from server.speagle.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='Your Email')
    password = forms.CharField(widget=forms.PasswordInput)

