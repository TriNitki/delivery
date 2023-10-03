import pytest
import json

from .model_factories import UserFactory, UserUpdateFactory
from .conftest import UserCompareBase, Client, compare_models
from app.main import app
from app.user.schemas import UserCreateBase, UserDisplay, UserUpdateBase

@pytest.fixture(scope='class')
def new_user():
    return UserFactory.build()

@pytest.fixture(scope='session')
def user_update_body():
    return UserUpdateFactory.build()

class TestUser:
    client = Client(app)
    
    def test_signup_user(self, new_user: UserCreateBase):
        self.client.signup(new_user)
    
    def test_login_user(self, new_user: UserCreateBase):
        self.client.login(new_user.email, new_user.password)
    
    def test_refresh_tokens(self):
        self.client.refresh_tokens()
    
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
        
        response_blank = UserUpdateBase(**json.loads(response.read()))
        assert response_blank
        
        assert UserUpdateBase(**new_user.model_dump()) == UserUpdateBase(**response_blank.model_dump())  # noqa: E501
        
        # Random user update
        response = self.client.patch(
            '/user/me', content=user_update_body.model_dump_json()
        )
        assert response.status_code == 200
        response_user = UserUpdateBase(**json.loads(response.read()))
        assert response_user
        assert compare_models(user_update_body, response_user)

    def test_deactivate_me(self):
        response = self.client.delete('/user/me')
        assert response.status_code == 200
        
        response = self.client.get('/user/me')
        assert response.status_code == 400
