from sqlalchemy import (Column, UUID, String, Boolean, DateTime, Integer, 
                        DECIMAL, SmallInteger, event, func, Enum, Interval)
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship, Mapped
from typing import List

from .database import Base, SessionLocal
from .schemas import RussianCitiesEnum, Genders, Roles, CountriesEnum

def generate_product_id(context):
    session = SessionLocal.object_session(context)
    max_value = session.query(func.max(DbProduct.id)).scalar()
    current_max = max_value or 0
    return f"{int(current_max) + 1:06d}"

def generate_order_id(context):
    session = SessionLocal.object_session(context)
    max_value = session.query(func.max(DbOrder.id)).scalar()
    current_max = max_value or 0
    return f"{int(current_max) + 1:06d}"

class DbUser(Base):
    __tablename__: str = 'users'
    id = Column(UUID, primary_key=True, default=uuid4, unique=True)
    email = Column(String, primary_key=True, unique=True)
    full_name = Column(String)
    phone_number = Column(String, nullable=True)
    gender = Column(Enum(Genders), nullable=True)
    date_of_birth = Column(DateTime)
    city = Column(Enum(RussianCitiesEnum))
    currency_name = Column(String, default="RUB")
    profile_picture = Column(String(128), nullable=True)
    role = Column(Enum(Roles), default="BUYER")
    password = Column(String)
    balance = Column(DECIMAL, default=0)
    registration_datetime = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_registered = Column(Boolean, default=True)
    
    products = relationship("DbProduct", back_populates='seller')
    favorites = relationship("DbFavorite")
    cart = relationship("DbCart")
    orders = relationship("DbOrder", back_populates="buyer")
    sales = relationship("DbOrderProduct", back_populates="seller")
    # currency = relationship("DbCurrency", back_populates='user')


class DbOrder(Base):
    __tablename__: str = 'orders'
    id = Column(String(6), default=generate_order_id, primary_key=True, unique=True)
    buyer_id = Column(UUID, ForeignKey('users.id'))
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    delivery_address = Column(String(256))
    
    products = relationship("DbOrderProduct", back_populates="order_details")
    buyer = relationship("DbUser", back_populates="orders")
    

class DbOrderProduct(Base):
    __tablename__: str = 'order_products'
    details_id = Column(String(6), ForeignKey('orders.id'), primary_key=True)
    id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    name = Column(String(128))
    price = Column(DECIMAL)
    weight = Column(Integer)
    manufacturer_country = Column(Enum(CountriesEnum))
    category_name = Column(String)
    brand = Column(String(32))
    discount = Column(SmallInteger, default=0)
    description = Column(String(1024), nullable=True)
    image = Column(String(128), nullable=True)
    seller_id = Column(UUID, ForeignKey('users.id'))
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    
    quantity = Column(Integer)
    delivery_datetime = Column(DateTime)
    estimated_delivery_time = Column(Interval)
    is_cancelled = Column(Boolean, default=False)
    
    warehouse = relationship("DbWarehouse", back_populates='orders')
    seller = relationship("DbUser", back_populates='sales')
    product = relationship("DbProduct")
    order_details = relationship("DbOrder", back_populates='products')


class DbStock(Base):
    __tablename__: str = 'stocks'
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), primary_key=True)
    units_in_stock = Column(Integer)
    
    product = relationship("DbProduct", back_populates='stock', uselist=False)


class DbReview(Base):
    __tablename__: str = 'reviews'
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    description = Column(String(1024), nullable=True)
    publication_datetime = Column(DateTime, default=datetime.utcnow)
    rating = Column(SmallInteger)
    
    product = relationship("DbProduct", back_populates='reviews')
    owner = relationship("DbUser")

     
class DbFavorite(Base):
    __tablename__: str = 'favorites'
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    addition_datetime = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("DbProduct")


class DbCurrency(Base):
    __tablename__: str = 'currencies'
    name = Column(Enum(CountriesEnum), primary_key=True)
    rate_to_usd = Column(DECIMAL)
    last_update = Column(DateTime)
    
    # user = relationship("DbUser", back_populates='currency')


class DbProduct(Base):
    __tablename__: str = 'products'
    id = Column(String(6), default=generate_product_id, primary_key=True, unique=True)
    name = Column(String(128))
    price = Column(DECIMAL)
    weight = Column(Integer)
    manufacturer_country = Column(Enum(CountriesEnum))
    category_name = Column(String)
    brand = Column(String(32))
    discount = Column(SmallInteger, default=0)
    description = Column(String(1024), nullable=True)
    image = Column(String(128), nullable=True)
    is_active = Column(Boolean, default=True)
    seller_id = Column(UUID, ForeignKey('users.id'))
    
    reviews = relationship('DbReview', back_populates='product')
    seller = relationship("DbUser", back_populates='products')
    stock: Mapped[List[DbStock]] = relationship("DbStock", back_populates='product', uselist=False)  # noqa: E501


class DbCart(Base):
    __tablename__: str = 'carts'
    user_id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    product_id = Column(String(6), ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)
    addition_datetime = Column(DateTime, default=datetime.utcnow)
    
    product: Mapped[DbProduct] = relationship("DbProduct", uselist=False)


class DbWarehouse(Base):
    __tablename__: str = 'warehouses'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    address = Column(String(512), unique=True)
    packaging_time = Column(Interval)
    
    orders = relationship("DbOrderProduct", back_populates='warehouse')

@event.listens_for(DbProduct, 'before_insert')
def before_insert_listener_product(mapper, connection, target):
    target.id = generate_product_id(target)

@event.listens_for(DbOrder, 'before_insert')
def before_insert_listener_order(mapper, connection, target):
    target.id = generate_order_id(target)