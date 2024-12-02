from rest_framework import serializers
from .models import Cart, CartItem
from core.models import Product


class CartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    # Loose coupling considered here with dependency injection, simplicity considered
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
