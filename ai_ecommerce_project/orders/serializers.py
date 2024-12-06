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


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    order_number = serializers.CharField(read_only=True)
    

    def create(self, validated_data):
        """"""
        # Extract the items data from the validated data
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        # Create OrderItems and associate them with the order
        for item_data in items_data:
            product = item_data.get('product')  # Get the product from item_data
            price_per_unit = product.price if product else 0  # Fetch the price per unit
            total_price += price_per_unit * item_data['quantity']
            
            # Create OrderItem and associate it with the order
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price_per_unit=price_per_unit
            )
        
        # Update total_price of the order
        order.total_price = total_price
        order.save()
        
        return order

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_number', 'status', 'order_date', 'shipping_date', 'total_price', 'items']