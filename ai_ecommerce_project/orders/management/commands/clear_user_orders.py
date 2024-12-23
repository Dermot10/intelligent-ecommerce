from django.core.management.base import BaseCommand
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Clear all orders and related order items for a specific user."

    def add_arguments(self, parser):
        parser.add_argument(
            'username', 
            type=str, 
            help='Username of the user whose orders should be cleared'
        )

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            # Get the user
            user = User.objects.get(username=username)
            
            # Clear the orders
            orders = Order.objects.filter(user=user)
            order_ids = orders.values_list('id', flat=True)
            OrderItem.objects.filter(order_id__in=order_ids).delete()
            orders.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f"Cleared all orders and order items for user: {user.username}")
            )
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f"User with username '{username}' does not exist.")
            )
