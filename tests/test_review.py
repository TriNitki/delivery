import pytest
import json

from .model_factories import ReviewFactory, UserFactory
from .conftest import Client, compare_models
from app.main import app
from app.user.schemas import UserCreateBase
from app.review.schemas import ReviewDisplay, ReviewTestModel

@pytest.fixture(scope='class')
def new_user():
    return UserFactory.build()

@pytest.fixture(scope='class')
def new_review():
    return ReviewFactory.build()

class TestReview:
    client = Client(app)
    review = ReviewTestModel()
    
    def test_activate(self, new_user: UserCreateBase):
        self.client.signup(new_user)
        self.client.login(new_user.email, new_user.password)
        self.client.generate_new_product()
    
    def test_create(self):
        pass
    
    def test_get(self):
        pass
    
    def test_update(self):
        pass
    
    def test_delete(self):
        pass
    
    def test_deactivate(self):
        self.client.deactivate_product()
        self.client.deactivate()