import pytest
import re
import json

from .model_factories import UserFactory
from .conftest import client
from app.schemas.user import UserCreateBase, UserDisplay

@pytest.fixture(scope='session')
def new_user():
    return UserFactory.build()

class TestUser:
    jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
    client = client
    
    def login_user(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.client.post("/user/login", data=data)
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
        
        return response
    
    def refresh_token(self):
        response = self.client.post("/user/refresh")
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
        
        return response
         
    def __set_default_access_token(self, access_token):
        self.client.headers.setdefault("Authorization", f"Bearer {access_token}")
        
    
    def test_signup(self, new_user: UserCreateBase):
        response = self.client.post("/user/signup", content=new_user.model_dump_json())
        assert response.status_code == 200
        
        response_body = json.loads(response.read())

        assert UserDisplay(**response_body)
    
    def test_login(self, new_user: UserCreateBase):
        response = self.login_user(new_user.email, new_user.password)
        
        access_token = json.loads(response.read())['access_token']
        refresh_token = self.client.cookies.get('refresh_token')
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
    
    def test_refresh(self):
        refresh_response = self.refresh_token()
        
        access_token = json.loads(refresh_response.read())['access_token']
        refresh_token = self.client.cookies.get('refresh_token')
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
        
        
        
        
    