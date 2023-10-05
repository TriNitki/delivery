import pytest
import json

from .model_factories import (WarehouseFactory, UserFactory, WarehouseUpdateFactory,
                              StockFactory, StockModifyfactory)
from .conftest import Client, compare_models
from app.main import app
from app.user.schemas import UserCreateBase
from app.warehouse.schemas import (WarehouseTestModel, WarehouseDisplay, 
                                   WarehouseCreateBase, WarehouseUpdateBase, 
                                   StockCreatebase, StockDisplayBase, ModifyStock)

@pytest.fixture(scope='class')
def new_user():
    return UserFactory.build()

@pytest.fixture(scope='class')
def new_warehouse():
    return WarehouseFactory.build()

@pytest.fixture(scope='class')
def new_warehouse_update():
    return WarehouseUpdateFactory.build()

@pytest.fixture(scope='class')
def new_stock():
    return StockFactory.build()

@pytest.fixture(scope='class')
def new_set_stock():
    return StockFactory.build()

@pytest.fixture(scope='class')
def new_stock_modifier():
    return StockModifyfactory.build()

class TestWarehouse:
    client = Client(app)
    warehouse = WarehouseTestModel()
    
    def test_activate(self, new_user: UserCreateBase):
        self.client.signup(new_user)
        self.client.login(new_user.email, new_user.password)
        self.client.generate_new_product()
    
    def test_create(self, new_warehouse: WarehouseCreateBase):
        response = self.client.post(
            "/warehouse/", 
            content=new_warehouse.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = self.client.post("/warehouse/", content="{}")
        assert response_error.status_code == 422
        
        response_body = WarehouseDisplay(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_warehouse, response_body)
        self.warehouse.id = response_body.id
        
    
    def test_get(self, new_warehouse: WarehouseCreateBase):
        response = self.client.get(f"/warehouse/{self.warehouse.id}/")
        assert response.status_code == 200
        
        response_body = WarehouseDisplay(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_warehouse, response_body)
        
        
    def test_update(self, new_warehouse_update: WarehouseUpdateBase):
        response = self.client.patch(
            f"/warehouse/{self.warehouse.id}/", 
            content=new_warehouse_update.model_dump_json()
        )
        assert response.status_code == 200
        response_warehouse = WarehouseUpdateBase(**json.loads(response.read()))
        assert response_warehouse
        assert compare_models(new_warehouse_update, response_warehouse)
    
    def test_create_stock(self, new_stock: StockCreatebase):
        response = self.client.post(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}", 
            content=new_stock.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = self.client.post(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}", 
            content="{}"
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_stock, response_body)
        
    
    def test_get_stock(self, new_stock: StockCreatebase):
        response = self.client.get(
            f"/warehouse/{self.warehouse.id}/stock"
        )
        assert response.status_code == 200
        
        response_error = self.client.get(
            "/warehouse/-1/stock"
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**(json.loads(response.read())[0]))
        assert response_body
        assert compare_models(new_stock, response_body)
    
    def test_get_product_stock(self, new_stock: StockCreatebase):
        response = self.client.get(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}"
        )
        assert response.status_code == 200
        
        response_error = self.client.get(
            f"/warehouse/{self.warehouse.id}/stock/000"
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_stock, response_body)
    
    def test_modify_stock(self, new_stock: StockCreatebase, new_stock_modifier: ModifyStock):  # noqa: E501
        response = self.client.patch(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}",
            content=new_stock_modifier.model_dump_json()
        )
        assert response.status_code == 200
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        
        response_get = self.client.get(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}"
        )
        response_get_body = StockDisplayBase(**json.loads(response_get.read()))
        assert response_get_body
        assert compare_models(response_get_body, response_body)
        assert new_stock.units_in_stock + new_stock_modifier.modifier == response_get_body.units_in_stock  # noqa: E501
    
    def test_set_stock(self, new_set_stock: StockCreatebase):
        response = self.client.put(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}", 
            content=new_set_stock.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = self.client.post(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}", 
            content="{}"
        )
        assert response_error.status_code == 422
        
        response_get = self.client.get(
            f"/warehouse/{self.warehouse.id}/stock/{self.client.product.id}"
        )
        assert response_get.status_code == 200
        
        response_body = StockDisplayBase(**json.loads(response_get.read()))
        assert response_body
        assert compare_models(new_set_stock, response_body)
    
    def test_deactivate(self):
        self.client.deactivate_product()
        self.client.deactivate()
    