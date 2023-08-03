from uuid import UUID
from datetime import datetime, timedelta

from .models import DbOrder
from ...schemas.order import OrderCreateBase
from ...db.database import get_pg_db
from ..postgres import db_product

def create_order(id: UUID, product_id: str, request: OrderCreateBase) -> DbOrder:
    creation_datetime = datetime.now()
    db = get_pg_db()
    product = db_product.retrieve_product(next(db), product_id)
    
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
    
    return new_order