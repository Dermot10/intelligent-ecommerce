import os
import sys
import django

# Set up Django environment
sys.path.append("/Users/dermot/Development/Web_dev/intelligent_ecommerce/ai_ecommerce_project")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_ecommerce_project.settings")
django.setup()

# Import models after Django setup
from payments.models import Payment
from orders.models import Order
from django.contrib.auth import get_user_model

# Get a test user (replace with an actual user ID)
User = get_user_model()
user = User.objects.first()  # Get the first user in the DB (change this as needed)

if not user:
    print("No user found in the database. Create a user first.")
    sys.exit(1)

# Get the latest order for the user
order = Order.objects.filter(user=user).last()

if not order:
    print("No order found for this user.")
    sys.exit(1)

print(f"Latest Order: {order}")

# Check if there are payments for the order
payments = Payment.objects.filter(order=order)

if payments.exists():
    print(f"Payments found: {list(payments.values())}")
else:
    print("No payments found. Creating a test payment...")

    # Create a test payment
    payment = Payment.objects.create(
        order=order,
        user=user,
        payment_method="credit_card",
        payment_status="completed",
        transaction_id="test123",
        total_amount=100.00
    )
    
    print(f"Created Payment: {payment}")
