from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class FavoriteDisplay(BaseModel):
    user_id: UUID
    addition_datetime: datetime
    product_id: str