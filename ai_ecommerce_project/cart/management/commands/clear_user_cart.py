from django.core.management.base import BaseCommand
from cart.models import CartItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Clear the cart for a specific user"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user whose cart needs to be cleared')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            cleared_count = CartItem.objects.filter(cart__user=user).delete()
            self.stdout.write(
                self.style.SUCCESS(f"Cleared {cleared_count[0]} cart items for user: {user.username}")
            )
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with username '{username}' does not exist"))
