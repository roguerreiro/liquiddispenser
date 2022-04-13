from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    details = models.CharField(max_length=1000)
    image = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Dispenser(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    pin = models.IntegerField()

    def __str__(self):
        return "Dispenser " + str(self.id)

class Test(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return "Test #" + str(self.id) + " - " + str(self.value)
