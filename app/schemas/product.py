from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
import json
from uuid import UUID

with open('static\\countries.json') as f:
    countries_dict = {country["name"]: country["name"] for country in json.load(f)}

Countries = Enum('Countries', countries_dict)
    
class ProductCreateBase(BaseModel):
    price: Decimal
    weight: int
    manufacturer_country: Countries
    category_name: str
    brand: str
    discount: int | None = None
    description: str | None = None
    image: str | None = None
    
class ProductDisplayBase(ProductCreateBase):
    seller_id: UUID
    is_active: bool
    product_number: str
    
    