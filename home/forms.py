from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, label="الاسم الأول (بالعربيّة رجاءً)")
    username = forms.CharField(label='اسم المستخدم')
    password1 = forms.CharField(
        label="كلمة السر",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='<li>يجب أن تكون كلمة السر ثمانية حروف/أرقام على الأقل</li>'
                  '<li>يجب أن تحوي كلمة السر على حروف</li>',
    )
    password2 = forms.CharField(
        label="تأكيد كلمة السر",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="يرجى إدخال نفس كلمة السر السابفة",
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "username", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate'}),
                               label='اسم المستخدم')
    password = forms.CharField(widget=PasswordInput(), label='كلمة السر')
