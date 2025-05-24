from rest_framework import serializers
from ..models import Cart, CartItem
from .product import ProductSerializer
from ..models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartItemAddSerializer(serializers.Serializer):
    product = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)


class CartItemRemoveSerializer(serializers.Serializer):
    product = serializers.IntegerField(write_only=True)