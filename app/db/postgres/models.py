from sqlalchemy import (Column, UUID, String, Boolean, DateTime, Integer, 
                        DECIMAL, SmallInteger, event, func, Enum)
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from ..database import Base, SessionLocal
from ...schemas.unspecified import RussianCitiesEnum, Genders, Roles, CountriesEnum

def generate_padded_value(context):
    session = SessionLocal.object_session(context)
    max_value = session.query(func.max(DbProduct.id)).scalar()
    current_max = max_value or 0
    return f"{int(current_max) + 1:06d}"

class DbUser(Base):
    __tablename__: str = 'users'
    id = Column(UUID, primary_key=True, default=uuid4, unique=True)
    email = Column(String, primary_key=True, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    gender = Column(Enum(Genders), nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    city = Column(Enum(RussianCitiesEnum), nullable=False)
    currency_name = Column(String, default="RUB", nullable=False)
    profile_picture = Column(String, nullable=True)
    role = Column(Enum(Roles), default="BUYER", nullable=False)
    password = Column(String, nullable=False)
    balance = Column(DECIMAL, default=0, nullable=False)
    registration_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_registered = Column(Boolean, default=True, nullable=False)
    
    products = relationship("DbProduct", back_populates='seller')
    favorites = relationship("DbFavorite", back_populates='user')
    # currency = relationship("DbCurrency", back_populates='user')
    
class DbFavorite(Base):
    __tablename__: str = 'favorites'
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    addition_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("DbUser", back_populates='favorites')
    product = relationship("DbProduct", back_populates='favorited_by')
    

class DbCurrency(Base):
    __tablename__: str = 'currencies'
    name = Column(Enum(CountriesEnum), primary_key=True)
    rate_to_usd = Column(DECIMAL, nullable=False)
    last_update = Column(DateTime, nullable=False)
    
    # user = relationship("DbUser", back_populates='currency')
    
class DbProduct(Base):
    __tablename__: str = 'products'
    id = Column(String(6), default=generate_padded_value, primary_key=True, unique=True)
    name = Column(String(32), nullable=False)
    price = Column(DECIMAL, nullable=False)
    weight = Column(Integer, nullable=False)
    manufacturer_country = Column(Enum(CountriesEnum), nullable=False)
    category_name = Column(String, nullable=False)
    brand = Column(String(32), nullable=False)
    discount = Column(SmallInteger, default=0)
    description = Column(String(1024), nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    seller_id = Column(UUID, ForeignKey('users.id'))
    
    seller = relationship("DbUser", back_populates='products')
    stock = relationship("DbStock", back_populates='product', uselist=False)
    favorited_by = relationship("DbFavorite", back_populates='product')
    
class DbWarehouse(Base):
    __tablename__: str = 'warehouses'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    address = Column(String(512), unique=True)
    packaging_time = Column(Integer, nullable=False) # in hours
    

class DbStock(Base):
    __tablename__: str = 'stocks'
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    units_in_stock = Column(Integer, nullable=False)
    
    product = relationship("DbProduct", back_populates='stock', uselist=False)

@event.listens_for(DbProduct, 'before_insert')
def before_insert_listener(mapper, connection, target):
    target.id = generate_padded_value(target)