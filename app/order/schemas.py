from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from ..product.schemas import Product

class OrderCreateBase(BaseModel):
    delivery_address: str
    quantity: int
    creation_datetime: datetime | None = None

class OrderDisplay(BaseModel):
    user_id: UUID
    creation_datetime: datetime
    delivery_datetime: datetime
    estimated_delivery_time: int
    delivery_address: str
    product: Product
    quantity: int
    is_cancelled: bool

