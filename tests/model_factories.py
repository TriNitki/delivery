from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import PostGenerated

from app.user import schemas as user
from app.order import schemas as order
from app.product import schemas as product
from app.review import schemas as review

from app.warehouse import schemas as warehouse

class UserFactory(ModelFactory[user.UserCreateBase]):
    __model__ = user.UserCreateBase
    
    password_confirm = PostGenerated(lambda cls, data: data['password'])

class UserUpdateFactory(ModelFactory[user.UserUpdateBase]):
    __model__ = user.UserUpdateBase

class ProductFactory(ModelFactory[product.ProductCreateBase]):
    __model__ = product.ProductCreateBase

class ProductUpdateFactory(ModelFactory[product.ProductUpdateBase]):
    __model__ = product.ProductUpdateBase

class OrderFactory(ModelFactory[order.OrderCreateBase]):
    __model__ = order.OrderCreateBase

class ReviewFactory(ModelFactory[review.ReviewCreateBase]):
    __model__ = review.ReviewCreateBase

class ReviewUpdateFactory(ModelFactory[review.ReviewUpdateBase]):
    __model__ = review.ReviewUpdateBase

class WarehouseFactory(ModelFactory[warehouse.WarehouseCreateBase]):
    __model__ = warehouse.WarehouseCreateBase

class WarehouseUpdateFactory(ModelFactory[warehouse.WarehouseUpdateBase]):
    __model__ = warehouse.WarehouseUpdateBase

class StockFactory(ModelFactory[warehouse.StockCreatebase]):
    __model__ = warehouse.StockCreatebase

class StockModifyfactory(ModelFactory[warehouse.ModifyStock]):
    __model__ = warehouse.ModifyStock