from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class Roles(str, Enum):
    admin = "ADMIN"
    moderator = "MODERATOR"
    seller = "SELLER"
    buyer = "BUYER"

class Genders(str, Enum):
    male = "male"
    female = "female"
    
class Currencies(str, Enum):
    rub = "RUB"
    usd = "USD"
    eur = "EUR"

class UserCreateBase(BaseModel):
    email: str
    full_name: str
    password: str
    phone_number: str
    gender: Genders
    date_of_birth: datetime
    city: str
    currency: Currencies | None = None
    profile_picture: str

class UserUpdateBase(BaseModel):
    full_name: str | None = None
    password: str | None = None
    phone_number: str | None = None
    gender: Genders | None = None
    date_of_birth: datetime | None = None
    city: str | None = None
    currency: Currencies | None = None
    profile_picture: str | None = None
    role: Roles | None = None
    balance: float | None = None
    is_active: bool | None = None
    is_registered: bool | None = None
    
    

class UserDisplay(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone_number: str
    gender: Genders
    date_of_birth: datetime
    city: str
    currency: Currencies
    profile_picture: str
    role: Roles
    balance: float
    registration_datetime: datetime
    is_active: bool
    is_registered: bool