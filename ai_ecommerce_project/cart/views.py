from typing import Tuple, Optional, Union
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for managing the user's cart.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self) -> Union[Cart, None]:
        """
        Override to restrict carts to the authenticated user.
        """
        return Cart.objects.filter(user=self.request.user)

    def get_or_create_cart(self, user: User) -> Tuple[Cart, bool]:
        """
        Helper method to get or create a cart model for the authenticated user.
        """
        return Cart.objects.get_or_create(user=user)

    def validate_product_and_quantity(self, product_id: Optional[int],
                                      quantity: Optional[int]) -> Tuple[Optional[Product], Optional[str]]:
        if product_id is None:
            return "Product ID not found"
        if quantity is None or quantity <= 0:
            return "Quantity must be 1 or greater"

        try:
            product = Product.objects.get(id=product_id)
            return product, None
        except Product.DoesNotExist:
            return None, 'Product not found'

    def list(self, request, *args, **kwargs):
        """
        List the cart for the authenticated user.
        """
        cart, created = self.get_or_create_cart(request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Add an item to the authenticated user's cart.
        """
        cart, created = self.get_or_create_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product, error = self.validate_product_and_quantity(
            product_id, quantity)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        # if newly created cart item or increment quantity
        if item_created:
            cart_item.quantity = int(quantity)
        else:
            cart_item.quantity += int(quantity)

        cart_item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"], url_path="delete-cart")
    def delete_cart(self, request, *args, **kwargs) -> Response:
        """
        Deletes the authenticated user's cart and all associated items.
        """
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["delete"], url_path="delete-item/(?P<cart_item_id>\d+)")
    def delete_cart_item(self, request, *args, **kwargs) -> Response:
        """
        Deletes a specific item from the authenticated user's cart.
        """
        cart_item_id = kwargs.get("cart_item_id")

        # Try to find the CartItem, belonging to the authenticated user
        try:
            cart_item = CartItem.objects.get(
                id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'CartItem not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the CartItem
        cart_item.delete()

        return Response({'message': 'CartItem deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
