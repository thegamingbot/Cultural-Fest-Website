from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset

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

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Field('first_name', placeholder='First Name', style = "background-color: transparent"), 
            Field('last_name', placeholder='Last Name', style = "background-color: transparent"), 
            Field('email', placeholder='Email ID', style = "background-color: transparent"), 
            Field('username', placeholder='Username', style = "background-color: transparent"), 
            Field('password1', placeholder='Password', style = "background-color: transparent"), 
            Field('password2', placeholder='Password Confirmation', style = "background-color: transparent"), 

        )