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
from decimal import Decimal
import uuid
import logging 

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_cart_for_user(self, user):
        """
        Retrieve the user's cart, including items.
        """
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except Cart.DoesNotExist:
            return None
    
    def get_cart_items_for_user(self, user):
        """
        Retrieve all CartItems for the user's cart.
        """
        # Ensure the user has a cart
        cart = get_object_or_404(Cart, user=user)

        # Retrieve the CartItems associated with the cart
        cart_items = CartItem.objects.filter(cart=cart)

        return cart_items

    def get_serialized_cart_items(self, user):
        """
        Retrieve and serialize all CartItems for the user's cart.
        """
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()

        serializer = CartItemSerializer(cart_items, many=True)
        return serializer.data

    def calculate_order_total(self, cart_items):
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        # Apply taxes, discounts, or shipping if needed
        return total_price

    def create_order_number(self): 
        """Helper method to create order number for a given order"""
        order_number = uuid.uuid4().hex[:8].upper()
        return order_number

 
    def create(self, request, *args, **kwargs):
        """
        Create an order for the authenticated user based on their cart items.
        """
        user = request.user
        order_number = self.create_order_number()

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

    # def delete_order_item(self, request, *args, **kwargs ): 
    #     """Delete specific order item from user"""
    #     user = request.user
    #     order_number = kwargs.get('order_number')
    #     order_item_id = kwargs.get('order_item_id')

    #     order = get_object_or_404(Order, user=user, order_number=order_number)
    #     order_item = get_object_or_404(OrderItem, id=order_item_id, order=order)

    #     order.total_price -= order_item.quantity * order_item.price_per_unit 
    #     order_item.delete()
    #     order.save()
        
    #     return Response({f'message': 'order_item {order_item} was successfully deleted'}, status= status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['delete'])
    def delete_single_order(self, request, *args, **kwargs): 
        """Delete complete single order for user by id"""
        order = get_object_or_404(Order, user=request.user, id=request.order_id)
        order.items.all().delete()  # Should delete all related items
        order.delete()
                
        return Response({f'message': 'order {order.order_number} successfully deleted'}, status= status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def delete_all_orders(self, request, *args, **kwargs): 
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


    def list(self, request, *args, **kwargs):
        """Optional: Restrict orders to the logged-in user."""
        queryset = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

  