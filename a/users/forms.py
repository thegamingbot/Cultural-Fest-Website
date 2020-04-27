from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm (UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)

    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name','email', 'username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None