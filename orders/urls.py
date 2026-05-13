from django.urls import path
from .views import create_order, my_orders

urlpatterns = [
    path('create/', create_order),
    path('my/', my_orders),
]