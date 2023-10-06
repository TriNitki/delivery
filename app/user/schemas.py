from pydantic import BaseModel, EmailStr, constr, field_validator, Field
from pydantic_core.core_schema import FieldValidationInfo
from fastapi import HTTPException
from uuid import UUID
from datetime import datetime
from ..schemas import Genders, Currencies, Roles, RussianCitiesEnum
from ..static import url_regex

class UserCreateBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)
    password_confirm: str = Field(..., min_length=4)
    phone_number: constr(
        strip_whitespace=True,
        pattern=r"^(\+7|8)[0-9]{10}$",
    )
    gender: Genders
    date_of_birth: datetime
    city: RussianCitiesEnum
    currency_name: Currencies = Currencies.rub
    profile_picture: constr(
        strip_whitespace=True,
        pattern=url_regex,
    ) = Field(..., examples=["https://example.com/"])
    
    @field_validator("password_confirm")
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise HTTPException(
                400, 'Passwords do not match'
            )
        return v

class LoginBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)

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

class UserTestModel(BaseModel):
    id: UUID | None = None
    email: str | None = None
    full_name: str | None = None
    phone_number: str | None = None
    gender: Genders | None = None
    date_of_birth: datetime | None = None
    city: RussianCitiesEnum | None = None
    currency_name: Currencies | None = None
    profile_picture: str | None = None
    role: Roles | None = None
    balance: float | None = None
    registration_datetime: datetime | None = None
    is_active: bool | None = None
    is_registered: bool | None = None
    password: str | None = None

class UserCompareBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: constr(
            strip_whitespace=True,
            pattern=r"^(\+7|8)[0-9]{10}$",
        )
    gender: Genders
    date_of_birth: datetime
    city: RussianCitiesEnum
    currency_name: Currencies = Currencies.rub
    profile_picture: str