from rest_framework import serializers
from .models import Cart, CartItem
from core.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    # Loose coupling considered here with dependency injection, simplicity considered
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
