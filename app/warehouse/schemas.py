from pydantic import BaseModel, Field
from datetime import timedelta

class WarehouseCreateBase(BaseModel):
    address: str
    packaging_time: timedelta

class WarehouseDisplay(WarehouseCreateBase):
    id: int

class WarehouseUpdateBase(BaseModel):
    address: str | None = None
    packaging_time: timedelta | None = None

class WarehouseTestModel(BaseModel):
    id: str | None = None
    address: str | None = None
    packaging_time: timedelta | None = None

class StockCreatebase(BaseModel):
    units_in_stock: int = Field(..., ge=0)

class ModifyStock(BaseModel):
    modifier: int

class StockDisplayBase(BaseModel):
    warehouse_id: int
    product_id: str
    units_in_stock: int
    