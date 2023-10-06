import json

from .conftest import Client, compare_models
from app.main import app
from app.user.schemas import UserDisplay, UserUpdateBase

class TestUser:
    client = Client(app)
    
    def test_signup_user(self):
        self.client.signup()
    
    def test_login_user(self):
        self.client.login()
    
    def test_refresh_tokens(self):
        self.client.refresh_tokens()
    
    def test_retrieve_me(self):
        response = self.client.get('/user/me')
        assert response.status_code == 200
        
        response_body = UserDisplay(**json.loads(response.read()))
        assert response_body

        assert compare_models(self.client.user, response_body, ignore_none=True)
    
    def test_edit_me(self, user_update_body: UserUpdateBase):
        # Empty user update
        response = self.client.patch('/user/me', content='{}')
        assert response.status_code == 200
        
        response_blank = UserDisplay(**json.loads(response.read()))
        assert response_blank
        assert compare_models(self.client.user, response_blank)
        
        # Random user update
        response = self.client.patch(
            '/user/me', content=user_update_body.model_dump_json()
        )
        assert response.status_code == 200
        self.client.user.update(user_update_body)
        assert compare_models(self.client.user, user_update_body, ignore_none=True)

    def test_deactivate_me(self):
        response = self.client.delete('/user/me')
        assert response.status_code == 200
        
        response = self.client.get('/user/me')
        assert response.status_code == 400
