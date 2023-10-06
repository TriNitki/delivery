from typing import Annotated
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from . import db_favorite

from ..user.auth import Auth
from .schemas import FavoriteDisplay, UserFavoritesDisplay, FavoriteCreateBase
from ..user.schemas import UserDisplay
from ..user import db_user
from ..product.schemas import ProductDisplay
from ..database import get_pg_db
from ..dependencies import valid_product_id

router = APIRouter(
    prefix='/user',
    tags=['favorite']
)


@router.post('/favorite', response_model=FavoriteDisplay)
async def create_favorite(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    request: FavoriteCreateBase = Body(...)
):
    product = valid_product_id(request.product_id, db)
    return db_favorite.create_favorite(db, current_user.id, product.id)

@router.delete('/favorite/{product_id}', response_model=None)
async def delete_favorite(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product: Annotated[ProductDisplay, Depends(valid_product_id)]
):
    return db_favorite.delete_favorite(db, current_user.id, product.id)

@router.get('/favorites', response_model=UserFavoritesDisplay, response_model_by_alias=False)  # noqa: E501
async def get_user_favorites(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)]
):  
    return db_user.get_user_by_id(db, current_user.id)