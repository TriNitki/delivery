from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, LazyAttribute

from datetime import datetime
import random
import uuid

from app.db.postgres import models
from app.schemas import user

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.DbUser

    id = LazyAttribute(lambda _: uuid.uuid4())
    full_name = Faker("name")
    email = LazyAttribute(lambda _: '{}.{}@example.com'.format(*_.full_name.split()).lower())
    phone_number = Faker("phone_number")
    gender = LazyAttribute(lambda _: random.choice(list(user.Genders)))
    date_of_birth = Faker("date")
    city = "Moscow"
    currency_name = LazyAttribute(lambda _: random.choice(list(user.Currencies)))
    profile_picture = None
    role = LazyAttribute(lambda _: random.choice(list(user.Roles)))
    password = Faker("password")
    balance = LazyAttribute(lambda _: random.randint(0, 1000))
    registration_datetime = LazyAttribute(lambda _: datetime.utcnow())
    is_active = True
    is_registered = True