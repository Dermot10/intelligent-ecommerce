from .models import Order
from typing import Optional
from django.contrib.auth.models import User
import uuid


def get_latest_order_for_user(user: User) -> Optional[Order]: 
    return Order.objects.filter(user=user).order_by('-id', '-order_date').first()


def calculate_order_total(cart_items):
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    # Apply taxes, discounts, or shipping if needed
    return total_price

def create_order_number() -> int: 
    """Helper method to create order number for a given order"""
    order_number = uuid.uuid4().hex[:8].upper()
    return order_number