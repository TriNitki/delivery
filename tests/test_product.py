import pytest
import json

from .model_factories import ProductFactory, ProductUpdateFactory, UserFactory, WarehouseFactory
from .conftest import Client, compare_models
from app.main import app
from app.user.schemas import UserCreateBase
from app.product.schemas import ProductCreateBase, ProductUpdateBase, ProductDisplay, ProductTestModel, StockCreatebase, ModifyStock
from app.warehouse.schemas import WarehouseDisplay, WarehouseTestModel, WarehouseCreateBase

@pytest.fixture(scope='class')
def new_user():
    return UserFactory.build()

@pytest.fixture(scope='class')
def new_product():
    return ProductFactory.build()

@pytest.fixture(scope='class')
def new_warehouse():
    return WarehouseFactory.build()

@pytest.fixture(scope='session')
def product_update_body():
    return ProductUpdateFactory.build()

class TestProduct:
    client = Client(app)
    warehouse = WarehouseTestModel()
    product = ProductTestModel()
    
    def test_activate_user(self, new_user: UserCreateBase):
        self.client.signup(new_user)
        self.client.login(new_user.email, new_user.password)
    
    def test_create(self, new_product: ProductCreateBase):
        response = self.client.post("/product/", content=new_product.model_dump_json())
        assert response.status_code == 200
        
        response_error = self.client.post("/product/", content="{}")
        assert response_error.status_code == 422
        
        response_body = json.loads(response.read())
        assert response_body
        
        assert ProductDisplay(**response_body)
        assert ProductCreateBase(**response_body) == ProductCreateBase(**new_product.model_dump())
        
        self.product.id = response_body["id"]
    
    def test_get(self, new_product: ProductCreateBase):
        response = self.client.get(f"/product/{self.product.id}/")
        assert response.status_code == 200
        
        response_product = ProductDisplay(**json.loads(response.read()))
        assert response_product
        assert compare_models(new_product, response_product) 
    
    def test_update(
        self,
        product_update_body: ProductUpdateBase
    ):
        response = self.client.patch(
            f"/product/{self.product.id}/", 
            content=product_update_body.model_dump_json()
        )
        assert response.status_code == 200
        response_product = ProductUpdateBase(**json.loads(response.read()))
        assert response_product
        assert compare_models(product_update_body, response_product)
    
    def test_set_status(self):
        response_put = self.client.put(
            f"/product/{self.product.id}/status/", 
            content='{"is_active": false}'
        )
        assert response_put.status_code == 200
        
        response_get = self.client.get(f"/product/{self.product.id}/")
        assert response_get.status_code == 200
        assert json.loads(response_get.read())["is_active"] is False
    
    def test_create_stock(self, new_warehouse: WarehouseCreateBase):
        response_warehouse = self.client.post(
            "/warehouse", 
            content=new_warehouse.model_dump_json()
        )
        response_ware = WarehouseDisplay(**json.loads(response_warehouse.read()))
        self.warehouse.id = response_ware.id
        
        stock = StockCreatebase(units_in_stock=10, warehouse_id=self.warehouse.id)
        response_stock = self.client.post(
            f"/product/{self.product.id}/stock",
            content=stock.model_dump_json()
        )
        assert response_stock.status_code == 200
    
    def test_get_stock(self):
        response = self.client.get(
            f"/product/{self.product.id}/stock",
            
        )
        print(self.warehouse.id)
    
    def test_modify_stock(self):
        pass
    
    def test_set_stock(self):
        pass