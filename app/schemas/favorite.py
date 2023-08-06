from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class Favorite(BaseModel):
    addition_datetime: datetime
    product_id: str

class FavoriteDisplay(BaseModel):
    user_id: UUID
    addition_datetime: datetime
    product_id: str

class UserFavoritesDisplay(BaseModel):
    user_id: UUID
    favorites: List[Favorite] = []