from uuid import UUID
from datetime import datetime

from .models import DbCart
from ...schemas.cart import CartCreateBase

def create_cart(id: UUID, product_id: str, request: CartCreateBase):
    addition_datetime = datetime.utcnow()
    
    new_cart = DbCart.create(
        user_id=id,
        product_id=product_id,
        quantity=request.quantity,
        addition_datetime=addition_datetime
    )
    
    return new_cart

def get_user_cart(id: UUID):
    cart = DbCart.objects(user_id = id).all()[:]
    return {
        "user_id": id,
        "cart": [{
            "product_id": product["product_id"],
            "quantity": product["quantity"],
            "addition_datetime": product["addition_datetime"]
            } for product in cart]
    }