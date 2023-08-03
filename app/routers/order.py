from typing import Annotated
from fastapi import APIRouter, Depends
import cassandra.cluster as cassandra

from ..db.jwt import JwtHandler
from ..schemas.order import OrderCreateBase, OrderDisplay
from ..schemas.product import Product
from ..schemas.user import UserDisplay
from ..db.cassandra import db_order

router = APIRouter(
    prefix='/user/order/{product_number}',
    tags=['order']
)

@router.post('/', response_model=OrderDisplay)
async def create_order(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str,
    request: OrderCreateBase
):
    order = db_order.create_order(current_user.id, product_id, request)
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