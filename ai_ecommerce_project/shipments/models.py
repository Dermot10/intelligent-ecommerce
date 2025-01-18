from django.db import models
from core.models import Product
from orders.models import Order

class Shipments(models.Model):
    shipping_id = models.AutoField(primary_key=True)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    card_transaction_time = models.DateTimeField()  # Timestamp of the card transaction
    packing_time = models.DateTimeField()  # Timestamp when the product was packed
    shipping_order_time = models.DateTimeField()  # Timestamp when the shipping order was placed

    def __str__(self):
        return f"Shipment {self.shipping_id} for Order {self.order}"

