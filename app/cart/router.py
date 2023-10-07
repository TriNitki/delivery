from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import Union

from . import db_cart

from ..user.auth import Auth
from ..user.schemas import UserDisplay
from .schemas import CartDisplay, UserCartDisplay
from ..user import db_user
from ..database import get_pg_db

router = APIRouter(
    prefix='/user/cart',
    tags=['cart']
)

@router.get('/', response_model=UserCartDisplay, response_model_by_alias=False)
async def get_user_cart(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
):
    return db_user.get_user_by_id(db, current_user.id)


@router.post('/', response_model=CartDisplay)
async def create_cart(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Body(embed=True)
):
    return db_cart.create_cart(db, current_user.id, product_id)

@router.patch('/{product_id}', response_model=Union[CartDisplay, None])
async def modify_cart_amount(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path(),
    modifier: int = Body(embed=True)
):
    return db_cart.modify_cart_amount(db, current_user.id, product_id, modifier)

@router.delete('/{product_id}', response_model=None)
async def delete_cart_product(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_cart.delete_cart_product(db, current_user.id, product_id)