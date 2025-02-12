from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Product
from orders.models import Order, OrderItem
from .models import Payment
import logging


logger = logging.getLogger(__name__)

class PaymentSerializer(serializers.ModelSerializer): 
    payment_status = serializers.ChoiceField(choices=Payment.payment_choices)
    
    class Meta:   
        model = Payment
        fields = ['user', 'order', 'payment_method', 'payment_status', 'transaction_id', 'total_amount', 'payment_date']
        read_only_fields = ['transaction_id', 'payment_date']