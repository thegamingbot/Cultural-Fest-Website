from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    ID =  models.CharField(primary_key=True, max_length = 4)
    Name = models.CharField(max_length = 64)
    Cost = models.IntegerField()

    def __str__(self):
        return f"Name: {self.Name} | Cost: {self.Cost}"

class Cart(models.Model):
    Name = models.CharField(primary_key=True, max_length = 64)
    Events = models.ManyToManyField(Event, blank=True)
    Accomodation = models.BooleanField()

    def __str__(self):
        return f"{self.Name}"

class Registered(models.Model):
    Name = models.CharField(primary_key=True, max_length = 64)
    Cart = models.ManyToManyField(Cart, blank=True)
    Events = models.ManyToManyField(Event, blank=True)
    Accomodation = models.BooleanField()
    def __str__(self):
        return f"{self.Name}"

class notRegistered(models.Model):
    Name = models.CharField(primary_key=True, max_length = 64)
    Events = models.ManyToManyField(Event, blank=True)
    Accomodation = models.BooleanField()
    def __str__(self):
        return f"{self.Name}"

class invoice(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

class pdf(models.Model):
    Name = models.CharField(primary_key=True, max_length = 64)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
