import json

from .conftest import Client, compare_models
from app.main import app
from app.review.schemas import ReviewDisplay, ReviewCreateBase, ReviewUpdateBase

class TestReview:
    client = Client(app)
    
    def test_activate(self):
        self.client.signup()
        self.client.login()
        self.client.generate_new_product()
    
    def test_review_create(self, new_review: ReviewCreateBase):
        response = self.client.post(
            f"/product/{self.client.product.id}/review", 
            content=new_review.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = self.client.post(
            f"/product/{self.client.product.id}/review", 
            content="{}"
        )
        assert response_error.status_code == 422
        
        response_body = ReviewDisplay(**json.loads(response.read()))
        
        assert response_body
        assert compare_models(new_review, response_body)
    
    def test_review_get(self, new_review: ReviewCreateBase):
        response = self.client.get(
            f"/product/{self.client.product.id}/reviews"
        )
        assert response.status_code == 200
        reviews = json.loads(response.read())
        response_body = [
            ReviewDisplay(**review) for review in reviews 
            if review["reviewer"]["id"] == str(self.client.user.id)
        ][0]
        assert response_body
        assert compare_models(new_review, response_body)
    
    def test_review_update(self, new_update_review: ReviewUpdateBase):
        response = self.client.patch(
            f"/product/{self.client.product.id}/review",
            content=new_update_review.model_dump_json()
        )
        assert response.status_code == 200
        response_body = ReviewUpdateBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_update_review, response_body, ignore_none=True)
    
    def test_review_delete(self):
        response = self.client.delete(
            f"/product/{self.client.product.id}/review"
        )
        assert response.status_code == 200
        
        response_get = self.client.get(
            f"/product/{self.client.product.id}/reviews"
        )
        assert response.status_code == 200
        response_get_content = json.loads(response_get.read())
        assert not response_get_content or not any(
            [
                review["reviewer"]["id"] == str(self.client.user.id)
                for review in response_get_content
            ]
        )
    
    def test_deactivate(self):
        self.client.deactivate_product()
        self.client.deactivate()