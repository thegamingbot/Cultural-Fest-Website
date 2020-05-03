from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    ID =  models.CharField(primary_key=True, max_length = 4)
    Name = models.CharField(max_length = 64)
    Cost = models.IntegerField()

    def __str__(self):
        return f"ID: {self.ID}   Name: {self.Name}   Cost: {self.Cost}"

class SelectedEvent(models.Model):
    Name = models.ForeignKey(User, on_delete=models.CASCADE)
    Events = models.ManyToManyField(Event, blank=True)

