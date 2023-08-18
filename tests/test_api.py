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
    def login_user(self, user: UserCreateBase):
        data = {
            'username': user.email,
            'password': user.password,
        }
        
        response = client.post("/user/login", data=data)
        return response
    
    def test_signup(self, new_user: UserCreateBase):
        response = client.post("/user/signup", content=new_user.model_dump_json())
        response_body = json.loads(response.read())
        
        assert response.status_code == 200
        assert UserDisplay(**response_body)
    
    def test_login(self, new_user: UserCreateBase):
        response = self.login_user(new_user)
        response_body = json.loads(response.read())
        
        jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
        
        assert response.status_code == 200
        assert re.match(jwt_pattern, response_body['access_token'])
    
    