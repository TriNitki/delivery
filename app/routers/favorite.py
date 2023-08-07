from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query, Body
import cassandra.cluster as cassandra

from ..db.jwt import JwtHandler
from ..schemas.favorite import FavoriteDisplay, UserFavoritesDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_favorite

router = APIRouter(
    prefix='/user/favorite',
    tags=['favorite']
)

@router.post('/{product_id}', response_model=FavoriteDisplay)
async def create_favorite(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str = Path()
):
    return db_favorite.create_favorite(current_user.id, product_id)

@router.get('/', response_model=UserFavoritesDisplay)
async def get_user_favorites(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)]
):
    return db_favorite.get_user_favorites(current_user.id)