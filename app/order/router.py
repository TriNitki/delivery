from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
from datetime import datetime

from ..user.auth import Auth
from .schemas import OrderCreateBase, OrderDisplay
from ..user.schemas import UserDisplay
from . import db_order

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