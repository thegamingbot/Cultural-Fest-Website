from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from .forms import RegisterForm, EventForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, Cart, Registered, notRegistered
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template

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
            username = form1.cleaned_data.get('username')
            cart = Cart(Name=username, Accomodation=False)
            cart.save()
            registered = Registered(Name=username, Accomodation=False)
            registered.save()
            notregistered = notRegistered(Name=username, Accomodation=true)
            notregistered.save()
            r = Event.objects.all()
            for event in r:
                notregistered.Events.add(event)
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
    user = User.objects.get(username = username)
    try:
        registered = Registered.objects.get(Name=username)
        cart = Cart.objects.get(Name=username)
        notregistered = notRegistered.objects.get(Name=username)
    except Registered.DoesNotExist:
        registered = Registered(Name=username, Accomodation=False)
        registered.save()
    except notRegistered.DoesNotExist:
        notregistered = notRegistered(Name=username, Accomodation=True)
        notregistered.save()
        r = Event.objects.all()
        for event in r:
            notregistered.Events.add(event)
    except Cart.DoesNotExist:
        cart = Cart(Name=username, Accomodation=False)
        cart.save()

    x = registered.Events.all()
    if user.id != id:
        raise Http404("Please login through the Register page..")
    
    event = Event.objects.all()
    
    form = EventForm(username, instance=cart)

    if request.method == 'POST' and 'cart' in request.POST:
        return HttpResponseRedirect(reverse("cart", args=(username, user.id)))

    if request.method == 'POST':
        form = EventForm(username, request.POST, instance=cart)
        if form.is_valid():
            form.save()
            q = Cart.objects.filter(Name=username)
            y = registered
            y.Cart.set(q)
            y.save()
            messages.success(request, 'Items added to your cart. You are being redirected to the cart right now.')
            return HttpResponseRedirect(reverse("cart", args=(username, user.id)))

    context = {
        "user":user,
        "event":event,
        "form":form,
        "cart":cart,
        "x":x,
        "registered":registered,
    }
    return render(request, "users/user.html", context)

def cart(request, username, id):
    user = User.objects.get(username = username)
    if user.id != id:
        raise Http404("Please login through the Register page..")
    try:
        cart = Cart.objects.get(Name=username)
        registered = Registered.objects.get(Name=username)
    except Cart.DoesNotExist:
        cart = Cart(Name=username, Accomodation=False)
    except Registered.DoesNotExist:
        registered = None

    if request.method == 'POST' and 'continue' in request.POST:
        return HttpResponseRedirect(reverse("user", args=(username, user.id)))

    if request.method == 'POST' and 'submit' in request.POST:
        x = cart.Events.all()
        notregistered = notRegistered.objects.get(Name=username)
        notregistered.delete()
        notregistered = notRegistered(Name=username, Accomodation=True)
        notregistered.save()
        for event in x:
            registered.Events.add(event)
        if cart.Accomodation ==True:
            registered.Accomodation = True
            registered.save()
        if registered.Accomodation == True:
            notregistered.Accomodation=False
            notregistered.save()
        x = registered.Events.all()
        y = Event.objects.all()
        z = y.difference(x)
        for event in z:
            notregistered.Events.add(event)
        x = Cart(Name=username, Accomodation=False)
        x.save()
        messages.success(request, 'Items are brought. You are being redirected to the user page right now.')
        return HttpResponseRedirect(reverse("user", args=(username, user.id)))
    
    x = 0
    z = cart
    y = z.Events.all()
    for a in y:
        x = x + a.Cost
    
    if z.Accomodation:
        x = x + 100

    context = {
        "user":user,
        "cart":cart,
        "y":y,
        "x":x,
        "z":z,
    }
    return render(request, "users/cart.html", context)

def genrate_pdf(request, *args, **kwargs):
    template=get_template("pdf/bill.html")
    context={
    "invoice_id":123,
    "customer_name":"Nikunj",
    "amount":123,
    }
    html=template.render(context)
    pdf=render_to_pdf("pdf/bill.html",context)
    return HttpResponse(pdf,content_type="application/pdf")
