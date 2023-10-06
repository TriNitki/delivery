from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID

from ..product.schemas import Product

class Favorite(BaseModel):
    addition_datetime: datetime
    product: Product

class FavoriteCreateBase(BaseModel):
    product_id: str

class FavoriteDisplay(BaseModel):
    user_id: UUID
    addition_datetime: datetime
    product_id: str

class UserFavoritesDisplay(BaseModel):
    user_id: UUID = Field(..., alias="id")
    favorites: List[Favorite] = []