from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label="Input your name", max_length=32)
    username = forms.CharField(label="Choose a username (Must be unique!)", max_length=32)
    password = forms.CharField(label="Enter your password", max_length=10, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Enter your password again", max_length=10, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")


class LoginForm(forms.Form):
    name = forms.CharField(label="Username", max_length=32)
    password = forms.CharField(label="Password", max_length=10, widget=forms.PasswordInput)
