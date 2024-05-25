from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    # is_active = forms.BooleanField(required=False, initial=True)
    # is_staff = forms.BooleanField(required=False, initial=True)
    # is_superuser = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')