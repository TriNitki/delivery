import json
import random

from .conftest import Client, compare_models
from app.main import app
from app.cart.schemas import CartDisplay, CartCreateBase

class TestCart:
    client = Client(app)
    
    def test_activate(self):
        self.client.signup()
        self.client.login()
        self.client.generate_new_product()
    
    def test_cart_create(self, new_cart: CartCreateBase):
        pass
    
    def test_cart_get(self):
        pass
    
    def test_cart_update(self):
        pass
    
    def test_cart_delete(self):
        pass
    
    def test_deactivate(self):
        self.client.deactivate_product()
        self.client.deactivate()