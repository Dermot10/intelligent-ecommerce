from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from orders.views import OrderViewSet
from .models import Payment
from .serializers import PaymentSerializer

import logging 

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def update_order_payment(self, user): 
        order = self.get_order_for_user(user)
