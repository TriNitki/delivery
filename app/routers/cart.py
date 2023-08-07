from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
import cassandra.cluster as cassandra

from ..db.jwt import JwtHandler
from ..schemas.user import UserDisplay
from ..schemas.cart import CartCreateBase, CartDisplay, UserCartDisplay
from ..db.cassandra import db_cart

router = APIRouter(
    prefix='/user/cart',
    tags=['cart']
)

@router.post('/{product_id}', response_model=CartDisplay)
async def create_cart(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str = Path(),
    request: CartCreateBase = Body()
):
    return db_cart.create_cart(current_user.id, product_id, request)

@router.get('/', response_model=UserCartDisplay)
async def get_user_cart(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)]
):
    return db_cart.get_user_cart(current_user.id)