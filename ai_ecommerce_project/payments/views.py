from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer
from .models import Payment

import logging 

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset = Payment.objects.all()
    serializer_class = ... #PaymentSerializer

    def get_order_for_user(self): 
        pass 

    def get_serializered_order_for_user(self): 
        pass

    def set_order_payment_pending(self): 
        pass 

    def update_order_payment_status(self): 
        pass 

