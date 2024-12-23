from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for managing the user's cart.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        """
        Override to restrict carts to the authenticated user.
        """
        return Cart.objects.filter(user=self.request.user)

    def get_or_create_cart(self, user):
        """
        Helper method to get or create a cart for the authenticated user.
        """
        return Cart.objects.get_or_create(user=user)
    

    def list(self, request, *args, **kwargs):
        """
        List the cart for the authenticated user.
        """
        cart, created = self.get_or_create_cart(request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Add an item to the authenticated user's cart.
        """
        cart, created = self.get_or_create_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST) 
            
        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        # if newly created cart item or increment quantity
        if item_created:
            cart_item.quantity = int(quantity)  
        else:
            cart_item.quantity = int(quantity) 

        cart_item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        Remove an item from the authenticated user's cart.
        """
        pk = kwargs.get('pk')
        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
