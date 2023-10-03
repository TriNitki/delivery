from ..schemas import CountriesEnum

from pydantic import BaseModel, field_validator, Field
from typing import List
from decimal import Decimal
from uuid import UUID

class StockCreatebase(BaseModel):
    warehouse_id: int
    units_in_stock: int = Field(..., ge=0)

class ModifyStock(BaseModel):
    modifier: int
    warehouse_id: int

class SetStatus(BaseModel):
    is_active: bool

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

class ProductTestModel(BaseModel):
    id: str | None = None
    name: str | None = None
    price: Decimal | None = None
    weight: int | None = None
    manufacturer_country: CountriesEnum | None = None
    category_name: str | None = None
    brand: str | None = None
    discount: int | None = None
    description: str | None = None
    image: str | None = None
    is_active: bool | None = None
    seller_id: UUID | None = None

class ProductCreateBase(BaseModel):
    name: str
    price: Decimal = Field(..., gt=0)
    weight: int = Field(..., gt=0)
    manufacturer_country: CountriesEnum
    category_name: str
    brand: str
    discount: int | None = Field(..., ge=0, le=100)
    description: str | None = None
    image: str | None = None
    
    @field_validator('discount')
    def set_discount(cls, discount):
        return discount or 0

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
    discount: int | None = 0
    description: str | None = None
    image: str | None = None
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
    description: str | None = None
    suggest: ProductSuggest