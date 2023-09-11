import pytest
import re
import json

from .model_factories import UserFactory, UserUpdateFactory
from .conftest import Client, UserCompareBase
from app.main import app
from app.schemas.user import UserCreateBase, UserDisplay, UserUpdateBase

@pytest.fixture(scope='session')
def new_user():
    return UserFactory.build()

@pytest.fixture(scope='session')
def user_update_body():
    return UserUpdateFactory.build()

class TestUser:
    jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
    client = Client(app)
    
    def test_signup_user(self, new_user: UserCreateBase):
        response = self.client.post("/user/signup", content=new_user.model_dump_json())
        assert response.status_code == 200
        
        response_body = json.loads(response.read())

        assert UserDisplay(**response_body)
    
    def test_login_user(self, new_user: UserCreateBase):
        self.client.login_user(new_user.email, new_user.password)
        
        access_token = self.client.get_access_token()
        refresh_token = self.client.get_refresh_token()
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
    
    def test_refresh_tokens(self):
        self.client.refresh_token()
        
        access_token = self.client.get_access_token()
        refresh_token = self.client.get_refresh_token()
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
    
    def test_retrieve_me(self, new_user: UserCreateBase):
        response = self.client.get('/user/me')
        assert response.status_code == 200
        
        response_body = json.loads(response.read())
        assert response_body
        
        assert UserDisplay(**response_body)
        assert UserCompareBase(**new_user.model_dump()) == UserCompareBase(**response_body)  # noqa: E501
    
    def test_edit_me(self, new_user: UserCreateBase, user_update_body: UserUpdateBase):
        # Empty user update
        response = self.client.patch('/user/me', content='{}')
        assert response.status_code == 200
        
        response_body = json.loads(response.read())
        assert response_body
        
        assert UserDisplay(**response_body)
        assert UserCompareBase(**new_user.model_dump()) == UserCompareBase(**response_body)  # noqa: E501
        
        # Random user update
        response = self.client.patch(
            '/user/me', content=user_update_body.model_dump_json()
        )
        assert response.status_code == 200
        
        response_body = json.loads(response.read())
        assert response_body
        
        assert UserDisplay(**response_body)
        assert UserCompareBase(**new_user.model_dump()) != UserCompareBase(**response_body)  # noqa: E501
    
    def test_deactivate_me(self):
        response = self.client.delete('/user/me')
        assert response.status_code == 200
        
        response = self.client.get('/user/me')
        assert response.status_code == 400
        
        
    