from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem
from products.models import Product
from .serializers import CartSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return Response({"message": "Added to cart"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')

    item = CartItem.objects.get(id=item_id, user=request.user)
    item.quantity = quantity
    item.save()

    return Response({"message": "Updated"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    item = CartItem.objects.get(id=item_id, user=request.user)
    item.delete()

    return Response({"message": "Removed"})