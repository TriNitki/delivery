from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
import cassandra.cluster as cassandra

from ..db.jwt import JwtHandler
from ..schemas.user import UserDisplay
from ..schemas.cart import CartCreateBase, CartDisplay
from ..db.cassandra import db_cart

router = APIRouter(
    prefix='/user/cart/{product_id}',
    tags=['cart']
)

@router.post('/', response_model=CartDisplay)
async def create_order(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str = Path(),
    request: CartCreateBase = Body()
):
    return db_cart.create_cart(current_user.id, product_id, request)