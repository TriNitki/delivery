import json

from .conftest import Client, compare_models, ClientProduct
from app.main import app
from app.product.schemas import ProductCreateBase, ProductUpdateBase, ProductDisplay

class TestProduct:
    client = Client(app)
    
    def test_activate_user(self):
        self.client.signup()
        self.client.login()
    
    def test_create(self, new_product: ProductCreateBase):
        response = self.client.post("/product/", content=new_product.model_dump_json())
        assert response.status_code == 200
        
        response_error = self.client.post("/product/", content="{}")
        assert response_error.status_code == 422
        
        response_body = ProductDisplay(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_product, response_body)
        
        self.client.product = ClientProduct(**response_body.model_dump())
    
    def test_get(self, new_product: ProductCreateBase):
        response = self.client.get(f"/product/{self.client.product.id}/")
        assert response.status_code == 200
        
        response_product = ProductDisplay(**json.loads(response.read()))
        assert response_product
        assert compare_models(new_product, response_product) 
    
    def test_update(self, new_product_update: ProductUpdateBase):
        response = self.client.patch(
            f"/product/{self.client.product.id}/", 
            content=new_product_update.model_dump_json()
        )
        assert response.status_code == 200
        response_product = ProductDisplay(**json.loads(response.read()))
        assert response_product
        assert compare_models(new_product_update, response_product, ignore_none=True)
        
        self.client.product.update(response_product)
    
    def test_set_status(self):
        response_put = self.client.put(
            f"/product/{self.client.product.id}/status/", 
            content='{"is_active": false}'
        )
        assert response_put.status_code == 200
        
        response_get = self.client.get(f"/product/{self.client.product.id}/")
        assert response_get.status_code == 200
        assert json.loads(response_get.read())["is_active"] is False
    
    def test_deactivate_user(self):
        self.client.deactivate()