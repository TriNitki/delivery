from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from datetime import datetime
from fastapi import HTTPException

from .schemas import CartCreateBase
from ..models import DbCart

def _find_cart_item(db: Session, user_id: UUID, product_id: str):
    cart = db.query(DbCart).filter(
        and_(DbCart.user_id == user_id, DbCart.product_id == product_id)
    )
    
    if not cart.first():
        raise HTTPException(
            status_code=404,
            detail='The product was not found in the cart'
        )
    
    return cart

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

def modify_cart_amount(db: Session, user_id: UUID, product_id: str, modifier):
    cart = _find_cart_item(db, user_id, product_id)
    cart_item = cart.one()
    
    if cart_item.quantity + modifier <= 0:
        delete_cart_product(db, user_id, product_id)
        return None
    
    product_stock = sum(
        warehouse.units_in_stock for warehouse in cart_item.product.stock
    )
    
    if cart_item.quantity + modifier > product_stock:
        raise HTTPException(
            status_code=404,
            detail='Not enough product in stock'
        )
    
    cart.update({DbCart.quantity: DbCart.quantity + modifier})
    
    db.commit()
    
    return cart.one()
    
    
    

def delete_cart_product(db: Session, user_id: UUID, product_id: str):
    cart = _find_cart_item(db, user_id, product_id).first()
    
    db.delete(cart)
    db.commit()