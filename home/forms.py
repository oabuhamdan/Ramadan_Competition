from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput

from users.models import CustomUser, Competition


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="الاسم الثنائي (بالعربيّة رجاءً)")
    username = forms.CharField(label='اسم المستخدم', error_messages={
        'unique': "اسم المستخدم المدخل مستخدم سابقاً ، الرجاء إدخال اسم مستخدم آخر"})
    competition = forms.ModelChoiceField(queryset=Competition.objects.all(), label="المسابقة")

    def clean_username(self):
        return self.data.get('competition') + self.cleaned_data.get('username')

    class Meta:
        model = CustomUser
        fields = ["first_name", "username", "password1", "password2", "competition"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate'}),
                               label='اسم المستخدم')
    password = forms.CharField(widget=PasswordInput(), label='كلمة السر')
    competition = forms.ModelChoiceField(queryset=Competition.objects.all(), label="المسابقة")
    error_messages = {
        'invalid_login': (
            "الرجاء التأكد من صحة اسم المستخدم وكلمة المرور ، وفي حال نسيتهما ، الرجاء التواصل مع مشرفك"
        )
    }

    def clean_username(self):
        return self.data.get('competition') + self.cleaned_data.get('username')
