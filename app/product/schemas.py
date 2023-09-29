from ..schemas import CountriesEnum

from pydantic import BaseModel
from typing import List
from decimal import Decimal
from uuid import UUID

class Stock(BaseModel):
    units_in_stock: int
    warehouse_id: int

class Product(BaseModel):
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
    is_active: bool
    seller_id: UUID

class ProductCreateBase(BaseModel):
    name: str
    price: Decimal
    weight: int
    manufacturer_country: CountriesEnum
    category_name: str
    brand: str
    discount: int | None = None
    description: str | None = None
    image: str | None = None

class ProductUpdateBase(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    weight: int | None = None
    manufacturer_country: CountriesEnum | None = None
    category_name: str | None = None
    brand: str | None = None
    discount: int | None = None
    description: str | None = None
    image: str | None = None
    
class ProductDisplay(BaseModel):
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
    is_active: bool
    seller_id: UUID
    
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
    id: str
    name: str
    brand: str
    description: str
    suggest: ProductSuggest