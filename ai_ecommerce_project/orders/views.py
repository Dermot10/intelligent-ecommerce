from rest_framework import viewsets, status
from rest_framework.response import Response
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer
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

    def calculate_order_total(self, cart_items):
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        # Apply taxes, discounts, or shipping if needed
        return total_price


    # def perform_create(self, serializer):
    #     cart = self.get_cart_for_user(self.request.user)
    #     cart_items = cart.items.all()
    #     logger.info(f"Cart items retrieved: {cart_items}")
    #     order_number = uuid.uuid4().hex[:8].upper()
        
    #     if not cart_items:
    #         return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     total_price = self.calculate_order_total(cart_items)

    #     # Create the order
    #     order = serializer.save(user=self.request.user, order_number=order_number, total_price=total_price)
    #     logger.info(f"Order created successfully: {order}")

    #     order_data = {
    #         "user": self.request.user,
    #         "order_number": order_number,
    #     }
    #     logger.debug(f"Order creation data: {order_data}")
        
    #     # Populate OrderItem from CartItem
    #     for item in cart_items:
    #         OrderItem.objects.create(
    #             order=order,
    #             product=item.product,
    #             quantity=item.quantity,
    #             price_per_unit=item.product.price
    #         )
    #         logger.info(f"Processing cart item: {item}")

    #     # Clear the cart
    #     cart.items.all().delete()
    #     logger.info("Cart cleared successfully")

    def perform_create(self, serializer):
        cart = self.get_cart_for_user(self.request.user)
        cart_items = cart.items.all()

        logger.info(f"Cart items retrieved: {cart_items}")
        order_number = uuid.uuid4().hex[:8].upper()

        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare items data for the serializer
        items_data = [
            {
                'product': item.product,
                'quantity': item.quantity,
            } for item in cart_items
        ]

        # Create the order with items
        order = serializer.save(
            user=self.request.user,
            order_number=order_number,
            items=items_data  # Pass the items data explicitly to the serializer
        )

        logger.info(f"Order created successfully: {order}")

        # Clear the cart after creating the order
        cart.items.all().delete()
        logger.info("Cart cleared successfully")


    def list(self, request, *args, **kwargs):
        """Optional: Restrict orders to the logged-in user."""
        queryset = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
