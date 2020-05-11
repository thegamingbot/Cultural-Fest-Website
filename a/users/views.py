from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from .forms import RegisterForm, EventForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, Cart, Registered, notRegistered, Person
from django.views.generic import View
from .utils import *
from django.template.loader import get_template
import datetime
from django.core.mail import EmailMessage

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
            person = Person(Name = username, loggedin = False)
            person.save()
            cart = Cart(Name=username, Accomodation=False)
            cart.save()
            registered = Registered(Name=username, Accomodation=False)
            registered.save()
            notregistered = notRegistered(Name=username, Accomodation=True)
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
                person = Person.objects.get(Name=username)
                person.loggedin = True
                person.save()
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
    person = Person.objects.get(Name=username)
    if person.loggedin == True:
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

        if request.method == 'POST' and 'print' in request.POST:
            return HttpResponseRedirect(reverse("pdf", args=(username, user.id)))

        if request.method == 'POST' and 'cart' in request.POST:
            return HttpResponseRedirect(reverse("cart", args=(username, user.id)))

        if request.method == 'POST' and 'logout' in request.POST:
            person = Person.objects.get(Name=username)
            person.loggedin = False
            person.save()
            return HttpResponseRedirect(reverse("register"))

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
    else:
        raise Http404("Please login through the Register page..")

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

def genrate_pdf(request, username, id, *args, **kwargs):
    template=get_template("pdf/bill.html")
    user = User.objects.get(username=username)
    registered = Registered.objects.get(Name=username)
    x = registered.Events.all()
    y = 0
    for a in x:
        y = y + a.Cost
    if registered.Accomodation:
        y = y + 100
    date = datetime.date.today()
    context={
        "user":user,
        "registered":registered,
        "x":x,
        "y":y,
        "date":date,
    }
    html=template.render(context)
    pdf=render_to_pdf("pdf/bill.html",context)
    a = HttpResponseRedirect(reverse("pdf", args=(username, id)))
    subject = 'Shadow Cultural Fest Invoice'
    message = 'Greetings,\n\n     This mail is a confirmation of your payments in Shadow Cultural Fest. Use our website(http://shadowcf.pythonanywhere.com/) to download a copy of the invoice for furture reference. Hope you have all your expectations met here. Please free to mail us at shadow.culturalfest@gmail.com, for any queries.\n\nThank you,\nShadow team.'
    frommail = 'shadow.culturalfest@gmail.com'
    tomail = [user.email,]
    email = EmailMessage(subject, message, frommail, tomail)
    #email.attach_file("static/Images/bill.jpg")
    email.attach_file("out.pdf")
    email.send()
    return HttpResponse(pdf, content_type="application/pdf")
