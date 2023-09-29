from sqlalchemy.orm.session import Session
from uuid import UUID
from typing import List

from .schemas import OrderDetails
from ..models import DbOrder, DbOrderProduct

def create_order(
    db: Session, 
    user_id: UUID, 
    order_details: List[OrderDetails], 
    delivery_addres: str
):
    new_order = DbOrder(
        buyer_id=user_id,
        delivery_address=delivery_addres
    )
    
    db.add(new_order)
    db.commit()
    
    create_order_product(db, new_order.id, order_details)
    
    db.refresh(new_order)
    
    return new_order

def get_order(db: Session, order_id: str):
    return db.query(DbOrder).filter(DbOrder.id == order_id).first()

def create_order_product(db: Session, details_id, order_details: List[OrderDetails]):
    objects = [
        DbOrderProduct(
            id=order_product.id,
            details_id=details_id,
            name=order_product.name,
            price=order_product.price,
            weight=order_product.weight,
            manufacturer_country=order_product.manufacturer_country,
            category_name=order_product.category_name,
            brand=order_product.brand,
            discount=order_product.discount,
            description=order_product.description,
            image=order_product.image,
            seller_id=order_product.seller.id,
            warehouse_id=order_product.warehouse.id,
            quantity=order_product.quantity,
            delivery_datetime=order_product.delivery_datetime,
            estimated_delivery_time=order_product.estimated_delivery_time
        ) for order_product in order_details
    ]
    
    db.bulk_save_objects(objects)
    db.commit()