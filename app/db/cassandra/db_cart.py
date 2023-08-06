from uuid import UUID
from datetime import datetime

from .models import DbCart
from ...schemas.cart import CartCreateBase

def create_cart(id: UUID, product_id: str, request: CartCreateBase):
    addition_datetime = datetime.now()
    
    new_cart = DbCart.create(
        user_id=id,
        product_id=product_id,
        quantity=request.quantity,
        addition_datetime=addition_datetime
    )
    
    return new_cart