import typing
import httpx
import json
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from starlette.types import ASGIApp
from fastapi.testclient import TestClient

from app.schemas.unspecified import RussianCitiesEnum, Genders, Currencies

class Client(TestClient):
    def __init__(self, app: ASGIApp, base_url: str = "http://testserver", raise_server_exceptions: bool = True, root_path: str = "", backend: str = "asyncio", backend_options: typing.Dict[str, typing.Any] | None = None, cookies: httpx._client.CookieTypes = None, headers: typing.Dict[str, str] = None) -> None:
        super().__init__(app, base_url, raise_server_exceptions, root_path, backend, backend_options, cookies, headers)
    
    def login_user(self, username: str, password: str):
        data = {
            'username': username,
            'password': password,
        }
        
        response = self.post("/user/login", data=data)
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
    
    def refresh_token(self):
        response = self.post("/user/refresh")
        assert response.status_code == 200
        
        self.__set_default_access_token(json.loads(response.read())['access_token'])
    
    def get_access_token(self):
        return self.headers.get("Authorization").split()[1]
    
    def get_refresh_token(self):
        return self.cookies.get('refresh_token')
         
    def __set_default_access_token(self, access_token: str):
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