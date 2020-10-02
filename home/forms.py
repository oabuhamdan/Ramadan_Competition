from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32)

    class Meta:
        model = CustomUser
        fields = ["first_name", "username", "password1", "password2"]
