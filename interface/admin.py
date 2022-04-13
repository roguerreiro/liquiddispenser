from django.contrib import admin

from .models import Product, Dispenser, Test

# Register your models here.
admin.site.register(Product)
admin.site.register(Dispenser)
admin.site.register(Test)
