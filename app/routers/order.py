from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
import cassandra.cluster as cassandra
from datetime import datetime

from ..db.jwt import JwtHandler
from ..schemas.order import OrderCreateBase, OrderDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_order

router = APIRouter(
    prefix='/user/order/{product_id}',
    tags=['order']
)

@router.post('/', response_model=OrderDisplay)
async def create_order(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str = Path(),
    request: OrderCreateBase = Body()
):
    return db_order.create_order(current_user.id, product_id, request)

@router.get('/', response_model=OrderDisplay)
async def get_order(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str = Path(),
    creation_datetime: datetime = Query()
    
):
    return db_order.get_order(current_user.id, product_id, creation_datetime)