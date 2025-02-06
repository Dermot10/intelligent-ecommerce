from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from .models import Payment
from .serializers import PaymentSerializer

import logging 

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['get'])
    def latest_order(self, request): 

        user = request.user
        order = Order.objects.filter(user=user).order_by('-order_date').first()
        if not order: 
            return Response({"detail: No orders found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def get_serialized_user_order(self, user): 

        order = self.get_latest_order_for_user(user)
        if not order: 
            return None
        serializer = OrderSerializer(order, many=True)
        return serializer

    def update_order_payment(self, user): 
        order = self.get_order_for_user(user)
