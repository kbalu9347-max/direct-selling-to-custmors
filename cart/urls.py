from django.urls import path
from .views import get_cart, add_to_cart, update_cart, remove_from_cart

urlpatterns = [
    path('', get_cart),
    path('add/', add_to_cart),
    path('update/', update_cart),
    path('remove/', remove_from_cart),
]