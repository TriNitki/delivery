from uuid import UUID
from sqlalchemy.orm.session import Session
from datetime import datetime

from ...schemas.cart import CartCreateBase
from .models import DbCart

def create_cart(db: Session, id: UUID, product_id: str, request: CartCreateBase):
    addition_datetime = datetime.utcnow()
    
    new_cart = DbCart(
        user_id = id,
        product_id = product_id,
        quantity = request.quantity,
        addition_datetime = addition_datetime
    )
    
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    
    return new_cart