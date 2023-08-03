from pydantic import BaseModel

class WarehouseCreateBase(BaseModel):
    address: str
    packaging_time: int

class WarehouseDisplay(WarehouseCreateBase):
    id: int