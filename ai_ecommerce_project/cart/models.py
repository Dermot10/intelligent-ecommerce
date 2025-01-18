from django.db import models
from django.contrib.auth.models import User
from core.models import Product


class Cart(models.Model):
    """Summary model for user Cart state"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart of {self.user.username}'


class CartItem(models.Model):
    """Transaction model for user's individual Cart items linked to a product"""
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items') 
        # related name allows for instances of CartItem model in relation to User to be retrieved with syntax items
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in cart of {self.cart.user.username}'
