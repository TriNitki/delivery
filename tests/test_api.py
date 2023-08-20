import typing
import httpx
import pytest
import re
import json
from starlette.types import ASGIApp

from .model_factories import UserFactory
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserCreateBase, UserDisplay

@pytest.fixture(scope='session')
def new_user():
    return UserFactory.build()

class Client(TestClient):
    def __init__(self, app: ASGIApp, base_url: str = "http://testserver", raise_server_exceptions: bool = True, root_path: str = "", backend: str = "asyncio", backend_options: typing.Dict[str, typing.Any] | None = None, cookies: httpx._client.CookieTypes = None, headers: typing.Dict[str, str] = None) -> None:
        super().__init__(app, base_url, raise_server_exceptions, root_path, backend, backend_options, cookies, headers)
    
    def login_user(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.post("/user/login", data=data)
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
        
        return response
    
    def refresh_token(self):
        response = self.post("/user/refresh")
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
        
        return response
         
    def __set_default_access_token(self, access_token):
        self.headers.setdefault("Authorization", f"Bearer {access_token}")
        

class TestUser:
    jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
    client = Client(app)
    
    def test_signup(self, new_user: UserCreateBase):
        response = self.client.post("/user/signup", content=new_user.model_dump_json())
        assert response.status_code == 200
        
        response_body = json.loads(response.read())

        assert UserDisplay(**response_body)
    
    def test_login(self, new_user: UserCreateBase):
        response = self.client.login_user(new_user.email, new_user.password)
        
        access_token = json.loads(response.read())['access_token']
        refresh_token = self.client.cookies.get('refresh_token')
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
    
    def test_refresh(self):
        refresh_response = self.client.refresh_token()
        
        access_token = json.loads(refresh_response.read())['access_token']
        refresh_token = self.client.cookies.get('refresh_token')
        
        print(self.client.get('/user/me').read())
        
        assert re.match(self.jwt_pattern, access_token)
        assert re.match(self.jwt_pattern, refresh_token)
        
        
        
        
    