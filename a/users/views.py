from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from .forms import RegisterForm, EventForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, SelectedEvent

# Create your views here.

def index(request):
    return render(request, "users/index.html")

def accomodation(request):
    return render(request, "users/accomodation.html")

def contact_us(request):
    return render(request, "users/contact_us.html")

def events(request):
    return render(request, "users/events.html")

def register(request):
    form1 = RegisterForm()
    form2 = AuthenticationForm()
    if request.method == "POST" and 'sign_up' in request.POST:
        form1 = RegisterForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request, 'Registered.. Voila!!')
    if request.method == "POST" and 'log_in' in request.POST:
        form2 = AuthenticationForm(request=request, data=request.POST)
        if form2.is_valid():
            username = form2.cleaned_data.get('username')
            password = form2.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user = User.objects.get(username = username)
                return HttpResponseRedirect(reverse("user", args=(username, user.id)))
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        form2 = AuthenticationForm()
    return render(request, "users/register.html", {"form1":form1, "form2":form2})

def schedule(request):
    return render(request, "users/schedule.html")

def sponsors(request):
    return render(request, "users/sponsors.html")

def user(request, username, id):
    form = EventForm()
    user = User.objects.get(username = username)
    try:
        select = SelectedEvent.objects.get(Name=username)
    except SelectedEvent.DoesNotExist:
        select = None

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.Name = username
            x.save()

    context = {
        "user":user,
        "form":form,
        "select":select,
    }
    return render(request, "users/user.html", context)
