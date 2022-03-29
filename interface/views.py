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

# Create your views here.
def index(request):
    dispensers = Dispenser.objects.all()
    return render(request, "interface/index.html", {
        "dispensers": dispensers
    })

def product(request, key):
    product = Product.objects.get(id=key)
    return render(request, "interface/product.html", {
        "product": product
    })

def checkout(request):
    return render(request, "interface/checkout.html")
