from typing import Annotated
from fastapi import APIRouter, Depends
import cassandra.cluster as cassandra

from ..db.jwt import JwtHandler
from ..schemas.favorite import FavoriteDisplay
from ..schemas.user import UserDisplay
from ..db.cassandra import db_favorite

router = APIRouter(
    prefix='/user/favorite/{product_number}',
    tags=['favorite']
)

@router.post('/', response_model=FavoriteDisplay)
async def create_favorite(
    current_user: Annotated[UserDisplay, Depends(JwtHandler.get_current_active_user)],
    product_id: str
):
    return db_favorite.create_favorite(current_user.id, product_id)