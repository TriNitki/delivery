from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from ..utils.auth import Auth
from ..schemas.favorite import FavoriteDisplay, UserFavoritesDisplay
from ..schemas.user import UserDisplay
from ..db.postgres import db_favorite
from ..db.database import get_pg_db

router = APIRouter(
    prefix='/user',
    tags=['favorite']
)


@router.post('/favorite/{product_id}', response_model=FavoriteDisplay)
async def create_favorite(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_favorite.create_favorite(db, current_user.id, product_id)

@router.delete('/favorite/{product_id}', response_model=None)
async def delete_favorite(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)],
    product_id: str = Path()
):
    return db_favorite.delete_favorite(db, current_user.id, product_id)

@router.get('/favorites', response_model=UserFavoritesDisplay, response_model_by_alias=False)
async def get_user_favorites(
    current_user: Annotated[UserDisplay, Depends(Auth.get_current_active_user)],
    db: Annotated[Session, Depends(get_pg_db)]
):  
    return db_favorite.get_favorites_by_user(db, current_user.id)