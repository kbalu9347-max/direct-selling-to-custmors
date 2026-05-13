from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    address = request.data.get('address')

    cart_items = CartItem.objects.filter(user=user)

    if not cart_items:
        return Response({"error": "Cart is empty"}, status=400)

    total_price = sum([item.product.price * item.quantity for item in cart_items])

    order = Order.objects.create(
        user=user,
        total_price=total_price,
        address=address
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    cart_items.delete()

    return Response({"message": "Order placed successfully"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)