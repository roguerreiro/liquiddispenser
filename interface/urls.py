from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:key>", views.product, name="product"),
    path("checkout", views.checkout, name="checkout"),
    path("dispense/<str:key>", views.dispense, name="dispense"),
    path("calibrate", views.calibrate, name="calibrate")
]
