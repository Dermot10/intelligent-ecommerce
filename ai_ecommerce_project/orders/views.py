from urllib import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from cart.models import Cart, CartItem
from cart.views import CartViewSet
from cart.serializers import CartItemSerializer
from .models import Order, OrderItem, Product
from .serializers import OrderSerializer
from .utils import get_latest_order_for_user, calculate_order_total, create_order_number
from decimal import Decimal
import logging 

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'])
    def latest_order(self, request) -> Response: 
        user = request.user
        order = get_latest_order_for_user(user)
        if not order: 
            return Response({"detail: No orders found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serialized_user_order(self, request) -> Response: 
        user = request.user
        order = get_latest_order_for_user(user)
        if not order: 
            return None
        serializered_order = OrderSerializer(order, many=True)
        return serializered_order
 
    def create(self, request, *args, **kwargs) -> Response:
        """
        Create an order for the authenticated user based on their cart items.
        """
        user = request.user
        order_number = create_order_number()

        # Step 1: Retrieve the user's cart
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            total_price=Decimal('0.0') # Will update after adding items
        )

        total_price = Decimal('0.0')

        # Create OrderItem entries from Cart items
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_per_unit=cart_item.product.price
            )
            total_price += cart_item.quantity * cart_item.product.price

        # Update the total price of the order
        order.total_price = total_price
        order.save()

        # Clear the cart
        cart.items.all().delete()

        # Serialize the Order object
        serializer = OrderSerializer(order)

        return Response(
            {'message': 'Order created successfully', 'order': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['delete'], url_path='delete_single_orderitem/(?P<order_item_id>\d+)')
    def delete_single_orderitem(self, request, *args, **kwargs) -> Response: 
        """Delete specific order item from user"""
        order = self.get_object()
        order_item_id = kwargs.get('order_item_id')

        # order = get_object_or_404(Order, user=request.user, order_number=order_number)
        order_item = get_object_or_404(OrderItem, id=order_item_id, order=order)

        order.total_price -= order_item.quantity * order_item.price_per_unit 
        order_item.delete()
        order.save()
        
        return Response({f'message': 'order_item {order_item} was successfully deleted'}, status= status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['delete'])
    def delete_single_order(self, request, *args, **kwargs) -> Response: 
        """Delete complete single order for user by id"""
        order = get_object_or_404(Order, user=request.user, id=request.order_id)
        order.items.all().delete()  # Should delete all related items
        order.delete()
                
        return Response({f'message': 'order {order.order_number} successfully deleted'}, status= status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def delete_all_orders(self, request, *args, **kwargs) -> Response: 
        """Delete all orders for user"""
        print("Request received for user:", request.user)
        orders = Order.objects.filter(user=request.user)

        print(f"Orders for user {request.user.username}: {orders}")
        if orders.exists(): 
            for order in orders: 
                order.items.all().delete()
            orders.delete()
                
            return Response({f'message': 'All orders for {user} have been successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({f'error': 'No orders for {user} found'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request, *args, **kwargs) -> Response:
        """Optional: Restrict orders to the logged-in user."""
        queryset = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

  