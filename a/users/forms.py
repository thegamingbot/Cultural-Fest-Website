from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Cart, Event, Registered, notRegistered

class RegisterForm (UserCreationForm):
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'autofocus': True}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    college = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'College'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "college", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name','email', 'username', "password1", "password2", 'college']:
            self.fields[fieldname].label = ''

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'

class EventForm(forms.ModelForm):
    Events = forms.ModelMultipleChoiceField(
                       widget = forms.CheckboxSelectMultiple,
                       queryset = Event.objects.all()
               )
    class Meta: 
        model = Cart
        exclude = ['Name']
        widgets = {
            'Events': forms.CheckboxInput(attrs={'class': 'form-control'})
        }

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        y = notRegistered.objects.get(Name=user)
        self.fields['Events'].queryset = y.Events.all()
        self.fields['Events'].label = ''
        if y.Accomodation == False:
            self.fields['Accomodation'].widget.attrs['disabled'] = True