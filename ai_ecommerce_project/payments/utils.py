from .models import Order
from typing import Optional
from django.contrib.auth.models import User
import uuid


def create_transaction_id() -> int: 
    """Helper method to create order number for a given order"""
    payment_number = uuid.uuid4().hex.upper() 
    return payment_number