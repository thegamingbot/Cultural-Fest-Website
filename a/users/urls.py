from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index()"),
    path("accomodation/", views.accomodation, name="accomodation()"),
    path("contact_us/", views.contact_us, name="contact_us()"),
    path("events/", views.events, name="events()"),
    path("register/", views.register, name="register()"),
    path("schedule/", views.schedule, name="schedule()"),
    path("sponsors/", views.sponsors, name="sponsors()"),
    path("index/", views.index, name="index()"),
    path("<username>/<int:id>", views.user, name="user"),
    path("<username>/<int:id>/cart/", views.cart, name='cart'),
    path("<username>/<id>", views.user, name="user"),
    path("<username>/<id>/pdf/",views.genrate_pdf, name="pdf"),
]

urlpatterns += staticfiles_urlpatterns()
