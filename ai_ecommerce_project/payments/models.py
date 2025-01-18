from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class Payment(models.Model):
    payment_choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)  
    payment_status = models.CharField(
        max_length=50,
        choices=payment_choices,
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # to store payment amount, get from the view/serialiser logic
    transaction_id = models.CharField(max_length=255, unique=True)  # unique transaction ID
    payment_date = models.DateTimeField(auto_now_add=True)  # auto set the payment date/time

    def __str__(self):
        return f"Payment {self.transaction_id} for Order {self.order.order_number}"
