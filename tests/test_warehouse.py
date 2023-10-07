import json

from .utils import Client, compare_models
from app.warehouse.schemas import (WarehouseTestModel, WarehouseDisplay, 
                                   WarehouseCreateBase, WarehouseUpdateBase, 
                                   StockCreatebase, StockDisplayBase, ModifyStock)

class TestWarehouse:
    warehouse = WarehouseTestModel()
    
    def test_create(self, client: Client, new_warehouse: WarehouseCreateBase):
        response = client.post(
            "/warehouse/", 
            content=new_warehouse.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = client.post("/warehouse/", json={})
        assert response_error.status_code == 422
        
        response_body = WarehouseDisplay(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_warehouse, response_body)
        self.warehouse.id = response_body.id
        
    
    def test_get(self, client: Client, new_warehouse: WarehouseCreateBase):
        response = client.get(f"/warehouse/{self.warehouse.id}/")
        assert response.status_code == 200
        
        response_body = WarehouseDisplay(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_warehouse, response_body)
        
        
    def test_update(self, client: Client, new_warehouse_update: WarehouseUpdateBase):
        response = client.patch(
            f"/warehouse/{self.warehouse.id}/", 
            content=new_warehouse_update.model_dump_json()
        )
        assert response.status_code == 200
        response_warehouse = WarehouseUpdateBase(**json.loads(response.read()))
        assert response_warehouse
        assert compare_models(new_warehouse_update, response_warehouse, ignore_none=True)  # noqa: E501
    
    def test_create_stock(self, client: Client, new_stock: StockCreatebase):
        new_stock.product_id = client.product.id
        response = client.post(
            f"/warehouse/{self.warehouse.id}/stock", 
            content=new_stock.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = client.post(
            f"/warehouse/{self.warehouse.id}/stock", 
            json={}
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_stock, response_body)
        
    
    def test_get_stock(self, client: Client, new_stock: StockCreatebase):
        response = client.get(
            f"/warehouse/{self.warehouse.id}/stock"
        )
        assert response.status_code == 200
        
        response_error = client.get(
            "/warehouse/-1/stock"
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**(json.loads(response.read())[0]))
        assert response_body
        assert compare_models(new_stock, response_body)
    
    def test_get_product_stock(self, client: Client, new_stock: StockCreatebase):
        response = client.get(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}"
        )
        assert response.status_code == 200
        
        response_error = client.get(
            f"/warehouse/{self.warehouse.id}/stock/000"
        )
        assert response_error.status_code == 422
        
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_stock, response_body)
    
    def test_modify_stock(self, client: Client, new_stock: StockCreatebase, new_stock_modifier: ModifyStock):  # noqa: E501
        response = client.patch(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}",
            content=new_stock_modifier.model_dump_json()
        )
        assert response.status_code == 200
        response_body = StockDisplayBase(**json.loads(response.read()))
        assert response_body
        
        response_get = client.get(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}"
        )
        response_get_body = StockDisplayBase(**json.loads(response_get.read()))
        assert response_get_body
        assert compare_models(response_get_body, response_body)
        assert new_stock.units_in_stock + new_stock_modifier.modifier == response_get_body.units_in_stock  # noqa: E501
    
    def test_set_stock(self, client: Client, new_set_stock: StockCreatebase):
        response = client.put(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}", 
            content=new_set_stock.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = client.put(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}", 
            json={}
        )
        assert response_error.status_code == 422
        
        response_get = client.get(
            f"/warehouse/{self.warehouse.id}/stock/{client.product.id}"
        )
        assert response_get.status_code == 200
        
        response_body = StockDisplayBase(**json.loads(response_get.read()))
        assert response_body
        assert compare_models(new_set_stock, response_body)
    