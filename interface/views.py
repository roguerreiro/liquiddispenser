# Import necessary libraries
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import datetime
from .models import Product, Dispenser, Test
import time
from .ultrasonic import distance, precise_distance, volume

# Declare dictionary that will store information on products dispensed by user
dispensed = {}
# timer = {}

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
            # timer[product.name] = [time.perf_counter()]
            # dispensed[product.name] = [0]
        return redirect("/dispense/" + key)
    else:
        return render(request, "interface/product.html", {
            "product": product
        })

def checkout(request):
    if request.method == "POST":
        dispensed.clear()
        return redirect("/test")
    items = []

    for item in dispensed.keys():
        if len(dispensed[item]) > 0:
            volume_dispensed = volume(dispensed[item][0]) - volume(dispensed[item][-1])
            # volume_dispensed = 1
            item_price = float(Product.objects.get(name=item).price)
            price = round(volume_dispensed * item_price, 2)
            volume_dispensed = round(volume_dispensed, 2)
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
        # timer[product.name].append(time.perf_counter())

        return redirect(index)
    else:
        return render(request, "interface/dispense.html", {
            "dispenser": dispenser
        })

def calibrate(request):
    if request.method == "POST":
        return redirect("/calibrate")
    readings = []
    readings_number = 3
    readings_sum = 0
    for i in range(readings_number):
        reading = precise_distance()
        # reading = i + 1
        readings.append([i + 1, reading])
        readings_sum += reading
        time.sleep(3)

    average = readings_sum / readings_number

    return render(request, "interface/calibrate.html", {
        "readings": readings,
        "average": average
    })

def test(request):
    if request.method == "POST":
        value = 0
        if request.POST.get('1'):
            value = 1
        elif request.POST.get('2'):
            value = 2
        elif request.POST.get('3'):
            value = 3
        elif request.POST.get('4'):
            value = 4
        elif request.POST.get('5'):
            value = 5
        # time = timer[-1] - timer[0]
        rating = Test(value=value, time=0)
        # timer = {}
        return redirect("/")
    else:
        return render(request, "interface/test.html")
