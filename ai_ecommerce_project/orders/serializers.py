from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Product
from .models import Order, OrderItem


#import logging


#logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Allow input

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_per_unit',]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'] = instance.quantity * instance.price_per_unit
        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    order_number = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_number', 'status', 'order_date', 'shipping_date', 'total_price', 'items']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert total_price to string for consistency
        representation['total_price'] = str(instance.total_price)
        return representation
   