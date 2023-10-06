import typing
import httpx
import json
import re
import pytest
from pydantic import BaseModel
from pydantic.config import ConfigDict
from starlette.types import ASGIApp
from fastapi.testclient import TestClient

from app.user.schemas import UserCreateBase, UserDisplay, UserTestModel, UserUpdateBase
from app.product.schemas import ProductTestModel, ProductUpdateBase
from . import model_factories as factories

@pytest.fixture(scope='class')
def new_user():
    return factories.UserFactory.build()

@pytest.fixture(scope='class')
def new_review():
    return factories.ReviewFactory.build()

@pytest.fixture(scope='session')
def new_update_review():
    return factories.ReviewUpdateFactory.build()

@pytest.fixture(scope='class')
def new_product():
    return factories.ProductFactory.build()

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

@pytest.fixture(scope='class')
def new_cart():
    return factories.CartFactory.build()

class ClientProduct(ProductTestModel):
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    
    def update(self, update_model: ProductUpdateBase):
        for attr, value in update_model.model_dump().items():
            if value is not None:
                setattr(self, attr, value)

class ClientUser(UserTestModel):
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    
    def update(self, update_model: UserUpdateBase):
        for attr, value in update_model.model_dump().items():
            if value is not None:
                setattr(self, attr, value)

class Client(TestClient):
    def __init__(
        self, 
        app: ASGIApp, 
        base_url: str = "http://testserver", 
        raise_server_exceptions: bool = True, 
        root_path: str = "", 
        backend: str = "asyncio", 
        backend_options: typing.Dict[str, typing.Any] | None = None, 
        cookies: httpx._client.CookieTypes = None, 
        headers: typing.Dict[str, str] = None
    ) -> None:
        super().__init__(
            app, base_url, raise_server_exceptions, root_path, 
            backend, backend_options, cookies, headers
        )
    
    _jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
    
    user = ClientUser()
    product = ClientProduct()
    
    def signup(self, create_base: UserCreateBase = None):
        if not create_base:
            create_base = factories.UserFactory.build()
        response = self.post("/user/signup", content=create_base.model_dump_json())
        assert response.status_code == 200
        
        response_body = json.loads(response.read())
        user_model = UserDisplay(**response_body)
        assert user_model
        
        self.user = ClientUser(**response_body, password = create_base.password)
    
    def login(self, username: str = None, password: str = None):
        if not all([username, password]):
            username = self.user.email
            password = self.user.password
            
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.post("/user/login", data=data)
        assert response.status_code == 200
        
        self._set_default_access_token(json.loads(response.read())['access_token'])
        self._verify_token_patterns()
    
    def deactivate(self):
        response = self.delete('/user/me')
        assert response.status_code == 200
    
    def refresh_tokens(self):
        response = self.post("/user/refresh")
        assert response.status_code == 200
        
        self._set_default_access_token(json.loads(response.read())['access_token'])
        self._verify_token_patterns()
    
    def get_access_token(self):
        return self.headers.get("Authorization").split()[1]
    
    def get_refresh_token(self):
        return self.cookies.get('refresh_token')
    
    def generate_new_product(self):
        new_product = factories.ProductFactory.build()
        response = self.post("/product/", content=new_product.model_dump_json())
        assert response.status_code == 200
        
        self.product = ClientProduct(**json.loads(response.read()))
    
    def deactivate_product(self):
        response = self.put(
            f"/product/{self.product.id}/status/", content='{"is_active": false}'
        )
        assert response.status_code == 200
        self.product = ClientProduct()
    
    def _verify_token_patterns(self):
        assert re.match(self._jwt_pattern, self.get_access_token())
        assert re.match(self._jwt_pattern, self.get_refresh_token())
    
    def _set_default_access_token(self, access_token: str):
        self.headers.setdefault("Authorization", f"Bearer {access_token}")

def compare_models(model_a: BaseModel, model_b: BaseModel, ignore_none: bool = False):
    '''
    Compares the same attributes of models
    '''
    for attr, value in model_a.model_dump().items():
        if hasattr(model_b, attr) and value != getattr(model_b, attr):
            if (value is None or not getattr(model_b, attr)) and not ignore_none:
                return False
    return True