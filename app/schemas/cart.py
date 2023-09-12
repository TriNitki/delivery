from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID

class Cart(BaseModel):
    product_id: str
    quantity: int
    addition_datetime: datetime

class CartCreateBase(BaseModel):
    quantity: int
    
class CartDisplay(BaseModel):
    addition_datetime: datetime
    user_id: UUID
    quantity: int
    product_id: str

class UserCartDisplay(BaseModel):
    user_id: UUID = Field(..., alias="id")
    cart: List[Cart] = []