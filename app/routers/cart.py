from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from ..utils.auth import Auth
from ..schemas.user import UserDisplay
from ..schemas.cart import CartCreateBase, CartDisplay, UserCartDisplay
from ..db.postgres import db_cart, db_user
from ..db.database import get_pg_db

router = APIRouter(
    prefix='/user/cart',
    tags=['cart']
)

@router.post('/{product_id}', response_model=CartDisplay)
async def create_cart(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    request: CartCreateBase = Body()
):
    return db_cart.create_cart(db, current_user.id, product_id, request)

@router.get('/', response_model=UserCartDisplay, response_model_by_alias=False)
async def get_user_cart(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
):
    return db_user.get_user_by_id(db, current_user.id)