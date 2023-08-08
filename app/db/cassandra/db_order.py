from uuid import UUID
from datetime import datetime, timedelta

from .models import DbOrder
from ...schemas.order import OrderCreateBase, OrderDisplay
from ...schemas.product import Product
from ...db.database import get_pg_db
from ..postgres import db_product

def create_order(id: UUID, product_id: str, request: OrderCreateBase) -> DbOrder:
    creation_datetime = datetime.utcnow() if request.creation_datetime is None else request.creation_datetime
    db = get_pg_db()
    product = db_product.get_product(next(db), product_id)
    
    '''
    Replace `delivery_datetime` and `estimated_delivery_time` values for not had coded variants
    '''
    
    new_order = DbOrder.create(
        user_id = id,
        creation_datetime = creation_datetime,
        delivery_datetime = creation_datetime + timedelta(days=5),
        estimated_delivery_time = 5,
        delivery_address = request.delivery_address,
        quantity = request.quantity,
        
        product_id = product_id,
        product_name = product.name,
        product_price = product.price,
        product_weight = product.weight,
        product_manufacturer_country = product.manufacturer_country,
        product_category_name = product.category_name,
        product_brand = product.brand,
        product_discount = product.discount,
        product_description = product.description,
        product_image = product.image,
        product_is_active = product.is_active,
        product_seller_id = product.seller_id
    )
    
    return __to_order_display(new_order)

def get_order(id: UUID, product_id: str, creation_datetime: datetime):
    order = DbOrder.get(user_id = id, product_id = product_id, creation_datetime = creation_datetime)
    
    return __to_order_display(order)


def __to_order_display(order: DbOrder):
    return OrderDisplay(
        user_id=order.user_id,
        creation_datetime=order.creation_datetime,
        delivery_datetime=order.delivery_datetime,
        estimated_delivery_time=order.estimated_delivery_time,
        delivery_address=order.delivery_address,
        quantity=order.quantity,
        is_cancelled=order.is_cancelled,
        product=Product(
            id=order.product_id,
            name=order.product_name,
            price=order.product_price,
            weight=order.product_weight,
            manufacturer_country=order.product_manufacturer_country,
            category_name=order.product_category_name,
            brand=order.product_brand,
            discount=order.product_discount,
            description=order.product_description,
            image=order.product_image,
            is_active=order.product_is_active,
            seller_id=order.product_seller_id
        )
    )