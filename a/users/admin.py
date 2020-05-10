from django.contrib import admin
from .models import Event, Cart, Registered, notRegistered, invoice

# Register your models here.
admin.site.register(Event)
admin.site.register(Cart)
admin.site.register(Registered)
admin.site.register(notRegistered)
admin.site.register(invoice)