from pydantic import BaseModel
from datetime import timedelta

class WarehouseCreateBase(BaseModel):
    address: str
    packaging_time: timedelta

class WarehouseDisplay(WarehouseCreateBase):
    id: int