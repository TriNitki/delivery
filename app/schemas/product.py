from pydantic import BaseModel, Extra
from typing import List, Dict
from decimal import Decimal
from enum import Enum
import json
from uuid import UUID

with open(r'app/static/countries.json') as f:
    countries_dict = {country["name"]: country["name"] for country in json.load(f)}

Countries = Enum('Countries', countries_dict)

class Stock(BaseModel):
    units_in_stock: int
    warehouse_id: int

class Product(BaseModel):
    id: str
    name: str
    price: Decimal
    weight: int
    manufacturer_country: Countries
    category_name: str
    brand: str
    discount: int
    description: str
    image: str
    is_active: bool
    seller_id: UUID

class ProductCreateBase(BaseModel):
    name: str
    price: Decimal
    weight: int
    manufacturer_country: Countries
    category_name: str
    brand: str
    discount: int | None = None
    description: str | None = None
    image: str | None = None
    stock: Stock
    
class ProductDisplay(BaseModel):
    id: str
    name: str
    price: Decimal
    weight: int
    manufacturer_country: Countries
    category_name: str
    brand: str
    discount: int
    description: str
    image: str
    is_active: bool
    seller_id: UUID
    stock: Stock
    
class ProductSearchDisplay(BaseModel):
    id: str | None = None
    name: str | None = None
    price: Decimal | None = None
    image: str | None = None

class ProductSearchResult(BaseModel):
    products: List[ProductSearchDisplay] | None = []

class ProductSuggest(BaseModel):
    input: List[str]
    weight: int

class ProductAutoComleteSearch(BaseModel):
    name: str
    brand: str
    description: str
    suggest: ProductSuggest