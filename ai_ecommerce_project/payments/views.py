from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from orders.views import OrderViewSet
from orders.utils import get_latest_order_for_user
from .models import Payment
from .serializers import PaymentSerializer

import logging 

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['patch', 'put'])
    def update_payment_status(self, request) -> Response: 
        user = request.user
        customer_order = get_latest_order_for_user(user)

        if not customer_order:
            return Response({"error": "No order found"}, status=status.HTTP_404_NOT_FOUND)

        if customer_order.status.lower() == "pending": 
            customer_order.status = "completed"
            customer_order.save()
            return Response({"message": "Payment status updated and now set to complete", "order_id" :{customer_order.id}})
     
        return Response({"error": "Order is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
            
