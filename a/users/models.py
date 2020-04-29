from django.db import models

# Create your models here.
class Events(models.Model):
    ID =  models.CharField(primary_key=True, max_length = 4)
    Name = models.CharField(max_length = 64)
    Cost = models.IntegerField()

    def __str__(self):
        return f"ID: {self.ID}   Name: {self.Name}   Cost: {self.Cost}"
