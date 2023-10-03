from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import UUID
from typing import List
from decimal import Decimal

from ..schemas import CountriesEnum
from ..user.schemas import MinUserDisplay
from ..warehouse.schemas import WarehouseDisplay

class OrderProductCreateBase(BaseModel):
    product_id: str
    warehouse_id: int
    quantity: int = Field(..., ge=1)
    
class OrderDetails(BaseModel):
    quantity: int
    delivery_datetime: datetime
    estimated_delivery_time: timedelta
    is_cancelled: bool
    id: str
    name: str
    price: Decimal
    weight: int
    manufacturer_country: CountriesEnum
    category_name: str
    brand: str
    discount: int
    description: str
    image: str
    warehouse: WarehouseDisplay
    seller: MinUserDisplay

class OrderCreateBase(BaseModel):
    delivery_address: str
    details: List[OrderProductCreateBase]

class OrderDisplay(BaseModel):
    id: str
    buyer_id: UUID
    delivery_address: str
    creation_datetime: datetime
    products: List[OrderDetails]
    

