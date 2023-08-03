from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CartCreateBase(BaseModel):
    quantity: int
    
class CartDisplay(CartCreateBase):
    addition_datetime: datetime
    user_id: UUID
    product_id: str