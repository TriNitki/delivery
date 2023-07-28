from sqlalchemy import Column, UUID, String, Boolean, DateTime, Integer, DECIMAL, SmallInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from ...db.database import Base

class CustomIncrement:
    def __init__(self):
        self.counter = 0

    def __get__(self, instance, owner):
        return f"{self.counter:06d}"

    def __set__(self, instance, value):
        raise AttributeError("Cannot set the value directly.")

    def increment(self):
        self.counter += 1

class CustomIncrementType(Integer):
    def __init__(self):
        super().__init__()

    def process_bind_param(self, value, dialect):
        return int(value)

    def process_result_value(self, value, dialect):
        return CustomIncrement()

class DbUser(Base):
    __tablename__: str = 'users'
    id = Column(UUID, primary_key=True, default=uuid4, unique=True, nullable=False)
    email = Column(String, primary_key=True, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    currency = Column(String, default="RUB", nullable=False)
    profile_picture = Column(String, nullable=True)
    role = Column(String, default="BUYER", nullable=False)
    password = Column(String, nullable=False)
    balance = Column(DECIMAL, default=0, nullable=False)
    registration_datetime = Column(DateTime, default=datetime.now, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_registered = Column(Boolean, default=True, nullable=False)
    
class DbProduct(Base):
    __tablename__: str = 'products'
    product_number = Column(CustomIncrementType, primary_key=True, unique=True, nullable=False)
    price = Column(DECIMAL, nullable=False)
    weight = Column(Integer, nullable=False)
    manufacturer_country = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    discount = Column(SmallInteger, default=0)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    seller_id = Column(UUID, ForeignKey('users.id'))
    
    