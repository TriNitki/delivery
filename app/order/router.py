from typing import Annotated, List
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm.session import Session

from ..database import get_pg_db
from ..user.auth import Auth
from .schemas import OrderDetails, OrderDisplay
from ..user.schemas import UserDisplay
from . import db_order

from ..schemas import Roles
from ..dependencies import valid_order_details, valid_order

router = APIRouter(
    prefix='/user/order',
    tags=['order']
)


@router.post('/', response_model=OrderDisplay)
async def create_order(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    order_details: Annotated[List[OrderDetails], Depends(valid_order_details)],
    db: Annotated[Session, Depends(get_pg_db)],
    delivery_address: str = Body()
):
    return db_order.create_order(db, current_user.id, order_details, delivery_address)

@router.get('/{order_id}', response_model=OrderDisplay)
async def get_order(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    order: Annotated[OrderDisplay, Depends(valid_order)],
):
    if current_user.role != Roles.admin and current_user.id != order.buyer_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this order"
        )
    
    return order