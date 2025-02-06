from .models import Cart, CartItem, Product
from typing import Optional, Tuple


def validate_product_and_quantity(product_id: Optional[int],
                                      quantity: Optional[int]) -> Tuple[Optional[Product], Optional[str]]:
    if product_id is None:
        return "Product ID not found"
    if quantity is None or quantity <= 0:
        return "Quantity must be 1 or greater"

    try:
        product = Product.objects.get(id=product_id)
        return product, None
    except Product.DoesNotExist:
        return None, 'Product not found'