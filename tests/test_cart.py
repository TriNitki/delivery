import json
import random

from .conftest import Client
from app.main import app
from app.cart.schemas import CartDisplay, Cart
from app.warehouse.schemas import WarehouseCreateBase, StockCreatebase

class TestCart:
    client = Client(app)
    
    def test_activate(self):
        self.client.signup()
        self.client.login()
        self.client.generate_new_product()
    
    def test_prepare(
        self, 
        new_warehouse: WarehouseCreateBase, 
        new_stock: StockCreatebase
    ):
        response_warehouse = self.client.post(
            "/warehouse/", 
            content=new_warehouse.model_dump_json()
        )
        assert response_warehouse.status_code == 200
        response_warehouse = json.loads(response_warehouse.read())
        
        new_stock.product_id = self.client.product.id
        new_stock.units_in_stock = 11
        response_stock = self.client.post(
            f"/warehouse/{response_warehouse['id']}/stock", 
            content=new_stock.model_dump_json()
        )
        assert response_stock.status_code == 200
    
    def test_cart_create(self):
        response = self.client.post(
            "/user/cart", 
            content=f'{{"product_id": "{self.client.product.id}"}}'
        )
        assert response.status_code == 200
        
        response_error = self.client.post("/user/cart", content="{}")
        assert response_error.status_code == 422
        
        response_body = CartDisplay(**json.loads(response.read()))
        assert response_body.quantity == 1
        assert response_body.product_id == self.client.product.id
        
    def test_cart_get(self):
        response = self.client.get("/user/cart")
        assert response.status_code == 200
        
        carts = json.loads(response.read())
        response_body = [
            Cart(**item) for item in carts["cart"]
            if item["product_id"] == self.client.product.id
        ][0]
        assert response_body.quantity == 1
        assert response_body.product_id == self.client.product.id

    def test_cart_update(self):
        modifier = random.randint(1, 10)
        response = self.client.patch(
            f"/user/cart/{self.client.product.id}", 
            content=f'{{"modifier": {modifier}}}'
        )
        assert response.status_code == 200
        
        response_error = self.client.patch(
            f"/user/cart/{self.client.product.id}", 
            content='{"modifier": 10}'
        )
        assert response_error.status_code == 400
        
        response_body = CartDisplay(**json.loads(response.read()))
        assert response_body
        assert 1 + modifier == response_body.quantity
    
    def test_cart_delete(self):
        response_delete = self.client.delete(f"/user/cart/{self.client.product.id}")
        assert response_delete.status_code == 200
        
        response_get = self.client.get("/user/cart")
        assert response_get.status_code == 200
        response_get_content = json.loads(response_get.read())
        assert not response_get_content or not any(
            [
                item["product_id"] == self.client.product.id
                for item in response_get_content["cart"]
            ]
        )
    
    def test_deactivate(self):
        self.client.deactivate_product()
        self.client.deactivate()