import json

from .utils import Client, compare_models
from app.user.schemas import UserDisplay, UserUpdateBase

class TestUser:    
    def test_refresh_tokens(self, client: Client):
        client.refresh_tokens()
    
    def test_retrieve_user(self, client: Client):
        response = client.get('/user/me')
        assert response.status_code == 200
        
        response_body = UserDisplay(**json.loads(response.read()))
        assert response_body

        assert compare_models(client.user, response_body, ignore_none=True)
    
    def test_edit_user(self, client: Client, user_update_body: UserUpdateBase):
        # Empty user update
        response = client.patch('/user/me', json={})
        assert response.status_code == 200
        
        response_blank = UserDisplay(**json.loads(response.read()))
        assert response_blank
        assert compare_models(client.user, response_blank)
        
        # Random user update
        response = client.patch(
            '/user/me', content=user_update_body.model_dump_json()
        )
        assert response.status_code == 200
        client.user.update(user_update_body)
        assert compare_models(client.user, user_update_body, ignore_none=True)

    def test_change_user_status(self, client: Client):
        response = client.put('/user/me/status', json={"is_active": False})
        assert response.status_code == 200
        
        response = client.get('/user/me')
        assert response.status_code == 400
        
        response = client.put('/user/me/status', json={"is_active": True})
        assert response.status_code == 200
        
        response = client.get('/user/me')
        assert response.status_code == 200
