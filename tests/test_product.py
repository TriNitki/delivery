import json

from .utils import Client, compare_models
from app.product.schemas import ProductUpdateBase, ProductDisplay

class TestProduct:
    def test_create(self, client: Client):
        response_error = client.post("/product/", json={})
        assert response_error.status_code == 422
    
    def test_get(self, client: Client):
        response = client.get(f"/product/{client.product.id}/")
        assert response.status_code == 200
        
        response_product = ProductDisplay(**json.loads(response.read()))
        assert response_product
        assert compare_models(client.product, response_product) 
    
    def test_update(self, client: Client, new_product_update: ProductUpdateBase):
        response = client.patch(
            f"/product/{client.product.id}/", 
            content=new_product_update.model_dump_json()
        )
        assert response.status_code == 200
        response_product = ProductDisplay(**json.loads(response.read()))
        assert response_product
        assert compare_models(new_product_update, response_product, ignore_none=True)
        
        client.product.update(response_product)
    
    def test_set_status(self, client: Client):
        response_put = client.put(
            f"/product/{client.product.id}/status/", 
            json={"is_active": False}
        )
        assert response_put.status_code == 200
        
        response_get = client.get(f"/product/{client.product.id}/")
        assert response_get.status_code == 200
        assert json.loads(response_get.read())["is_active"] is False
        
        response_put = client.put(
            f"/product/{client.product.id}/status/", 
            json={"is_active": True}
        )
        assert response_put.status_code == 200
        
        response_get = client.get(f"/product/{client.product.id}/")
        assert response_get.status_code == 200
        assert json.loads(response_get.read())["is_active"] is True