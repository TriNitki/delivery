import json
import random

from .utils import Client
from app.cart.schemas import CartDisplay, Cart
from app.warehouse.schemas import WarehouseCreateBase, StockCreatebase

class TestCart:    
    def test_prepare(
        self,
        client: Client,
        new_warehouse: WarehouseCreateBase, 
        new_stock: StockCreatebase
    ):
        response_warehouse = client.post(
            "/warehouse/", 
            content=new_warehouse.model_dump_json()
        )
        assert response_warehouse.status_code == 200
        response_warehouse = json.loads(response_warehouse.read())
        
        new_stock.product_id = client.product.id
        new_stock.units_in_stock = 11
        response_stock = client.post(
            f"/warehouse/{response_warehouse['id']}/stock", 
            content=new_stock.model_dump_json()
        )
        assert response_stock.status_code == 200
    
    def test_cart_create(self, client: Client):
        response = client.post("/user/cart", json={"product_id": client.product.id})
        assert response.status_code == 200
        
        response_error = client.post("/user/cart", json={})
        assert response_error.status_code == 422
        
        response_body = CartDisplay(**json.loads(response.read()))
        assert response_body.quantity == 1
        assert response_body.product_id == client.product.id
        
    def test_cart_get(self, client: Client):
        response = client.get("/user/cart")
        assert response.status_code == 200
        
        carts = json.loads(response.read())
        response_body = [
            Cart(**item) for item in carts["cart"]
            if item["product_id"] == client.product.id
        ][0]
        assert response_body.quantity == 1
        assert response_body.product_id == client.product.id

    def test_cart_update(self, client: Client):
        modifier = random.randint(1, 10)
        response = client.patch(
            f"/user/cart/{client.product.id}", 
            json={"modifier": modifier}
        )
        assert response.status_code == 200
        
        response_error = client.patch(
            f"/user/cart/{client.product.id}", 
            json={"modifier": 10}
        )
        assert response_error.status_code == 400
        
        response_body = CartDisplay(**json.loads(response.read()))
        assert response_body
        assert 1 + modifier == response_body.quantity
    
    def test_cart_delete(self, client: Client):
        response_delete = client.delete(f"/user/cart/{client.product.id}")
        assert response_delete.status_code == 200
        
        response_get = client.get("/user/cart")
        assert response_get.status_code == 200
        response_get_content = json.loads(response_get.read())
        assert not response_get_content or not any(
            [
                item["product_id"] == client.product.id
                for item in response_get_content["cart"]
            ]
        )