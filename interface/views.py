# Import necessary libraries
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import datetime
from .models import Product, Dispenser
from .ultrasonic import distance, precise_distance, volume

# Declare dictionary that will store information on products dispensed by user
dispensed = {}

# Create your views here.
def index(request):
    dispensers = Dispenser.objects.all()
    return render(request, "interface/index.html", {
        "dispensers": dispensers
    })

def product(request, key):
    product = Product.objects.get(id=key)
    dispenser = Dispenser.objects.get(product=product)
    if request.method == "POST":
        if product.name not in dispensed:
            dispensed[product.name] = [precise_distance()]
            # dispensed[product.name] = [0]
        return redirect("/dispense/" + key)
    else:
        return render(request, "interface/product.html", {
            "product": product
        })

def checkout(request):
    if request.method == "POST":
        dispensed.clear()
        return redirect("/")
    items = []

    for item in dispensed.keys():
        if len(dispensed[item]) > 0:
            volume_dispensed = volume(dispensed[item][0]) - volume(dispensed[item][-1])
            item_price = float(Product.objects.get(name=item).price)
            price = round(volume_dispensed * item_price, 2)
            items.append([item, volume_dispensed, price])

    return render(request, "interface/checkout.html", {
        "items": items
    })

def dispense(request, key):
    product = Product.objects.get(id=key)
    dispenser = Dispenser.objects.get(product=product)
    if request.method == "POST":
        dispensed[product.name].append(precise_distance())
        # dispensed[product.name].append(1)
        return redirect(index)
    else:
        return render(request, "interface/dispense.html", {
            "product": product
        })

def calibrate(request):
    if request.method == "POST":
        return redirect("/calibrate")
    reading = precise_distance()
    return render(request, "interface/calibrate.html", {
        "reading": reading
    })
