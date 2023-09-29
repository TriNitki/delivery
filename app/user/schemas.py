from pydantic import BaseModel, EmailStr, constr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from fastapi import HTTPException
from uuid import UUID
from datetime import datetime
from ..schemas import Genders, Currencies, Roles, RussianCitiesEnum

class UserCreateBase(BaseModel):
    email: EmailStr
    full_name: str
    password: constr(min_length=4)
    password_confirm: constr(min_length=4)
    phone_number: constr(
            strip_whitespace=True,
            pattern=r"^(\+7|8)[0-9]{10}$",
        )
    gender: Genders
    date_of_birth: datetime
    city: RussianCitiesEnum
    currency_name: Currencies = Currencies.rub
    profile_picture: str
    
    @field_validator("password_confirm")
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise HTTPException(
                400, 'Passwords do not match'
            )
        return v

class LoginBase(BaseModel):
    email: EmailStr
    password: constr(min_length=4)

class UserUpdateBase(BaseModel):
    full_name: str | None = None
    phone_number: constr(
            strip_whitespace=True,
            pattern=r"^(\+7|8)[0-9]{10}$",
        ) | None = None
    gender: Genders | None = None
    date_of_birth: datetime | None = None
    city: RussianCitiesEnum | None = None
    currency_name: Currencies | None = None
    profile_picture: str | None = None

class MinUserDisplay(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone_number: str
    profile_picture: str
    role: Roles
    is_active: bool
    is_registered: bool
    
class UserDisplay(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone_number: str
    gender: Genders
    date_of_birth: datetime
    city: RussianCitiesEnum
    currency_name: Currencies
    profile_picture: str
    role: Roles
    balance: float
    registration_datetime: datetime
    is_active: bool
    is_registered: bool