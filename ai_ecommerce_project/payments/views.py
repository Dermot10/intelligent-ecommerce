from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from orders.views import OrderViewSet
from orders.utils import get_latest_order_for_user
from .utils import create_transaction_id
from .models import Payment
from .serializers import PaymentSerializer

import logging 

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet): 
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def retrieve_order_payment(self, request) -> Response: 
        user = request.user
        customer_order = get_latest_order_for_user(user)
        # payment = Payment.objects.filter(order=customer_order)
        payment = Payment.objects.filter(order__order_number=customer_order.order_number)
        if not payment: 
            return Response({"error": "No Payment found"}, status=status.HTTP_404_NOT_FOUND)
        if not customer_order:
            return Response({"error": "No order found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(payment, many=True)  
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='retrieve_payment_by_id/(?P<transaction_id>[0-9A-Fa-f]+)')
    def retrieve_payment_by_id(self, request, *args, **kwargs) -> Response: 
        transaction_id = kwargs.get('transaction_id')
        payment = Payment.objects.filter(transaction_id=transaction_id)

        if not payment: 
            return Response({"error": "Transaction ID not found, payment not found"})
        serializer = self.get_serializer(payment, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_payments(self, request) -> Response: 
        queryset = Payment.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_payment(self, request) -> Response:
        if not request.user or not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        customer_order = get_latest_order_for_user(user)

        if not customer_order:
            return Response({"error": "No order found"}, status=status.HTTP_404_NOT_FOUND)
        transaction_id = create_transaction_id()

        payment = Payment.objects.create(
            order=customer_order,
            user=user,
            payment_method=request.data.get("payment_method", ""),  # Allow setting a method
            payment_status=customer_order.status,
            transaction_id=transaction_id,
            total_amount=customer_order.total_price
        )

        serializer = self.get_serializer(payment, many=False)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['patch', 'put'])
    def provide_payment_details(self, request, *args, **kwargs) -> Response: 
        user = request.user
        payment = Payment.objects.filter(user=user).first()
        if not payment: 
            return Response({"error": "No Payment found"}, status=status.HTTP_404_NOT_FOUND)
        payment_method = request.data.get('payment_method')
        if not payment_method:
            return Response({"error": "No payment method provided"}, status=status.HTTP_400_BAD_REQUEST)
        payment.payment_method = payment_method
        payment.save()
    
        return Response({"message": "Payment method updated successfully"})


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

    @action(detail=False, methods=['patch', 'put'])
    def cancel_user_payment(self, request) -> Response: 
        user = request.user
        customer_order = get_latest_order_for_user(user)
        payment = Payment.objects.filter(order=customer_order).first()

        if not payment:
            return Response({"error": f"No payment for order {customer_order.id} found"}, status=status.HTTP_404_NOT_FOUND)

        if payment.payment_status.lower() in ["pending", "completed"]:
            payment.payment_status = "cancelled"
            payment.save()
            return Response({"message": f"Payment for order - {customer_order.id}, has been successfully cancelled"})
     
        return Response({"error": "Order is not pending or completed"}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['patch', 'put'], url_path='cancel_payment/(?P<transaction_id>[0-9A-Fa-f]+)')
    def cancel_payment(self, request, *args, **kwargs) -> Response: 
        transaction_id = kwargs.get('transaction_id')
        payment = Payment.objects.filter(transaction_id=transaction_id).first()

        if not payment: 
            return Response({"error": "Transaction ID not found, payment not found"}, status=status.HTTP_404_NOT_FOUND)

        if payment.payment_status.lower() in ["pending", "completed"]: 
            payment.payment_status = "cancelled"
            payment.save()
            return Response({"message": f"Payment for transaction - {transaction_id}, has been successfully cancelled"})
     
        return Response({"error": "Payment is not pending or completed"}, status=status.HTTP_400_BAD_REQUEST)
