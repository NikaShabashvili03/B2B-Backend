from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import Cart, CartItem, Order, OrderItem, Customer, Product
from ..serializers.cart import CartItemAddSerializer, CartItemSerializer, CartItemRemoveSerializer
from ..serializers.order import OrderSerializer
from ..permissions import IsAuthenticated

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user
        cart, _ = Cart.objects.get_or_create(customer_id=customer.id)
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        customer = request.user
        cart, _ = Cart.objects.get_or_create(customer_id=customer.id)
        serializer = CartItemAddSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            
            product = get_object_or_404(Product, id=product_id)

            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            current_qty = cart_item.quantity if cart_item else 0
            total_quantity = current_qty + quantity

            if total_quantity > product.stock_quantity:
                return Response(
                    {'error': f'Requested quantity ({total_quantity}) exceeds available stock ({product.stock_quantity})'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if cart_item:
                cart_item.quantity = total_quantity
            else:
                cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            cart_item.save()

            return Response({'message': 'Added to cart'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer = request.user
        serializer = CartItemRemoveSerializer(data=request.data)

        if serializer.is_valid():
            product_id = serializer.validated_data['product']
            cart = get_object_or_404(Cart, customer_id=customer.id)
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
            return Response({'message': 'Item removed from cart'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

