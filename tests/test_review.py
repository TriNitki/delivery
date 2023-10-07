import json

from .utils import Client, compare_models
from app.review.schemas import ReviewDisplay, ReviewCreateBase, ReviewUpdateBase

class TestReview:    
    def test_review_create(self, client: Client, new_review: ReviewCreateBase):
        response = client.post(
            f"/product/{client.product.id}/review", 
            content=new_review.model_dump_json()
        )
        assert response.status_code == 200
        
        response_error = client.post(
            f"/product/{client.product.id}/review", 
            json={}
        )
        assert response_error.status_code == 422
        
        response_body = ReviewDisplay(**json.loads(response.read()))
        
        assert response_body
        assert compare_models(new_review, response_body)
    
    def test_review_get(self, client: Client, new_review: ReviewCreateBase):
        response = client.get(
            f"/product/{client.product.id}/reviews"
        )
        assert response.status_code == 200
        reviews = json.loads(response.read())
        response_body = [
            ReviewDisplay(**review) for review in reviews 
            if review["reviewer"]["id"] == str(client.user.id)
        ][0]
        assert response_body
        assert compare_models(new_review, response_body)
    
    def test_review_update(self, client: Client, new_update_review: ReviewUpdateBase):
        response = client.patch(
            f"/product/{client.product.id}/review",
            content=new_update_review.model_dump_json()
        )
        assert response.status_code == 200
        response_body = ReviewUpdateBase(**json.loads(response.read()))
        assert response_body
        assert compare_models(new_update_review, response_body, ignore_none=True)
    
    def test_review_delete(self, client: Client):
        response = client.delete(
            f"/product/{client.product.id}/review"
        )
        assert response.status_code == 200
        
        response_get = client.get(
            f"/product/{client.product.id}/reviews"
        )
        assert response.status_code == 200
        response_get_content = json.loads(response_get.read())
        assert not response_get_content or not any(
            [
                review["reviewer"]["id"] == str(client.user.id)
                for review in response_get_content
            ]
        )