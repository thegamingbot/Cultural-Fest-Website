from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index()"),
    path("accomodation.html/", views.accomodation, name="accomodation()"),
    path("contact_us.html/", views.contact_us, name="contact_us()"),
    path("events.html/", views.events, name="events()"),
    path("register.html/", views.register, name="register()"),
    path("schedule.html/", views.schedule, name="schedule()"),
    path("sponsors.html/", views.sponsors, name="sponsors()"),
    path("index.html/", views.index, name="index()")
]

urlpatterns += staticfiles_urlpatterns()
