import pytest

from . import model_factories as factories
from .utils import Client
from app.main import app

@pytest.fixture(scope='class')
def new_review():
    return factories.ReviewFactory.build()

@pytest.fixture(scope='session')
def new_update_review():
    return factories.ReviewUpdateFactory.build()

@pytest.fixture(scope='session')
def new_product_update():
    return factories.ProductUpdateFactory.build()

@pytest.fixture(scope='session')
def user_update_body():
    return factories.UserUpdateFactory.build()

@pytest.fixture(scope='class')
def new_warehouse():
    return factories.WarehouseFactory.build()

@pytest.fixture(scope='session')
def new_warehouse_update():
    return factories.WarehouseUpdateFactory.build()

@pytest.fixture(scope='class')
def new_stock():
    return factories.StockFactory.build()

@pytest.fixture(scope='session')
def new_set_stock():
    return factories.StockFactory.build()

@pytest.fixture(scope='session')
def new_stock_modifier():
    return factories.StockModifyfactory.build()

@pytest.fixture(scope="session")
def client():
    client = Client(app)
    client.signup()
    client.login()
    client.generate_new_product()
    return client