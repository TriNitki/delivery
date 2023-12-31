from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import PostGenerated

from app.schemas import (user, cart, warehouse,
                         product, review, order) 

class UserFactory(ModelFactory[user.UserCreateBase]):
    __model__ = user.UserCreateBase
    
    password_confirm = PostGenerated(lambda cls, data: data['password'])

class UserUpdateFactory(ModelFactory[user.UserUpdateBase]):
    __model__ = user.UserUpdateBase

class ProductFactory(ModelFactory[product.ProductCreateBase]):
    __model__ = product.ProductCreateBase

class OrderFactory(ModelFactory[order.OrderCreateBase]):
    __model__ = order.OrderCreateBase

class CartFactory(ModelFactory[cart.CartCreateBase]):
    __model__ = cart.CartCreateBase

class ReviewFactory(ModelFactory[review.ReviewCreateBase]):
    __model__ = review.ReviewCreateBase

class WarehouseFactory(ModelFactory[warehouse.WarehouseCreateBase]):
    __model__ = warehouse.WarehouseCreateBase