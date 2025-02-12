import os
import django
import sys

sys.path.append("/Users/dermot/Development/Web_dev/intelligent_ecommerce/ai_ecommerce_project")



# Set the settings module environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_ecommerce_project.settings")  # Replace with your project name

# Initialize Django
django.setup()
from orders.models import Order
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

user = User.objects.get(username="testuser999")  # Replace with actual username


"""Delete all orders for user by id"""
orders = Order.objects.filter(user=user)

if orders.exists(): 
    for order in orders: 
        order.items.all().delete()
    orders.delete()
        
    print({f'message': 'All orders for {request.user} have been successfully deleted'})
else: 
    print({f'error': 'No orders for {request.user} found'})

