from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Product
from orders.models import Order, OrderItem
from payments.models import Payment
from .models import Shipments
import logging


logger = logging.getLogger(__name__)

class ShipmentSerializer(serializers.ModelSerializer): 
    shipment_status = serializers.ChoiceField(choices=Order.status)
    transaction_id = serializers.SerializerMethodField()
    
    class Meta:   
        model = Shipments
        fields = ['shipping_id', 'order', 'product', 'shipment_status', 
          'transaction_id', 'card_transaction_time', 'packing_time', 'shipping_order_time']
        read_only_fields = ['transaction_id', 'card_transaction_time', 'packing_time', 'shipping_order_time']

    def get_transaction_id(self, obj):
        """Retrieve the transaction ID from the related Payment model"""
        payment = Payment.objects.filter(order=obj.order).first()  # Get the first payment for the order
        return payment.transaction_id if payment else None  # Return transaction_id if exists, else None