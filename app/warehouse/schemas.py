from pydantic import BaseModel
from datetime import timedelta

class WarehouseCreateBase(BaseModel):
    address: str
    packaging_time: timedelta

class WarehouseDisplay(WarehouseCreateBase):
    id: int

class WarehouseTestModel(BaseModel):
    id: str | None = None
    address: str | None = None
    packaging_time: timedelta | None = None