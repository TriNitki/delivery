import typing
import httpx
import json
import re
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from starlette.types import ASGIApp
from fastapi.testclient import TestClient

from app.schemas import RussianCitiesEnum, Genders, Currencies
from app.user.schemas import UserCreateBase, UserDisplay

class Client(TestClient):
    def __init__(
        self, 
        app: ASGIApp, 
        base_url: str = "http://testserver", 
        raise_server_exceptions: bool = True, 
        root_path: str = "", 
        backend: str = "asyncio", 
        backend_options: typing.Dict[str, typing.Any] | None = None, 
        cookies: httpx._client.CookieTypes = None, 
        headers: typing.Dict[str, str] = None
    ) -> None:
        super().__init__(
            app, base_url, raise_server_exceptions, root_path, 
            backend, backend_options, cookies, headers
        )
    
    _jwt_pattern = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$'
    
    def signup(self, create_base: UserCreateBase):
        response = self.post("/user/signup", content=create_base.model_dump_json())
        assert response.status_code == 200
        
        response_body = json.loads(response.read())

        assert UserDisplay(**response_body)
    
    def login(self, username: str, password: str):
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.post("/user/login", data=data)
        assert response.status_code == 200
        
        self._set_default_access_token(json.loads(response.read())['access_token'])
        self._verify_token_patterns()
    
    def refresh_tokens(self):
        response = self.post("/user/refresh")
        assert response.status_code == 200
        
        self._set_default_access_token(json.loads(response.read())['access_token'])
        self._verify_token_patterns()
    
    def get_access_token(self):
        return self.headers.get("Authorization").split()[1]
    
    def get_refresh_token(self):
        return self.cookies.get('refresh_token')
    
    def _verify_token_patterns(self):
        assert re.match(self._jwt_pattern, self.get_access_token())
        assert re.match(self._jwt_pattern, self.get_refresh_token())
    
    def _set_default_access_token(self, access_token: str):
        self.headers.setdefault("Authorization", f"Bearer {access_token}")

class UserCompareBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: constr(
            strip_whitespace=True,
            pattern=r"^(\+7|8)[0-9]{10}$",
        )
    gender: Genders
    date_of_birth: datetime
    city: RussianCitiesEnum
    currency_name: Currencies = Currencies.rub
    profile_picture: str

def compare_models(initial_model: BaseModel, response_model: BaseModel):
    for attr, value in initial_model.model_dump().items():
        if value is not None and value != getattr(response_model, attr):
            return False
    return True