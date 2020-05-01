from django.contrib import admin
from .models import Events, SelectedEvents

from .models import Events
# Register your models here.
admin.site.register(Events)
admin.site.register(SelectedEvents)