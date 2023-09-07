from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
from datetime import datetime

from ..utils.auth import Auth
from ..schemas.order import OrderCreateBase, OrderDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_order

router = APIRouter(
    prefix='/user/order',
    tags=['order']
)



@router.post('/{product_id}', response_model=OrderDisplay)
async def create_order(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    product_id: str = Path(),
    request: OrderCreateBase = Body()
):
    return db_order.create_order(current_user.id, product_id, request)

@router.get('/{product_id}', response_model=OrderDisplay)
async def get_order(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    product_id: str = Path(),
    creation_datetime: datetime = Query()
    
):
    return db_order.get_order(current_user.id, product_id, creation_datetime)