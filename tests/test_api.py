import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

from app.db.postgres import models
from app.db.database import Base
from .model_factories import UserFactory
from app.config import settings

engine = create_engine(settings.POSTGRES_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# this resets our tables in between each test
def _reset_schema():  
    db = SessionLocal()
    for table in Base.metadata.sorted_tables:
        db.execute(
            text(f'TRUNCATE {table.name} RESTART IDENTITY CASCADE;')
        )
        db.commit()

@pytest.fixture
def test_db():
    yield engine
    engine.dispose()
    '_reset_schema()'


@pytest.fixture
def session(test_db):
    connection = test_db.connect()
    transaction = connection.begin()
    db = scoped_session(sessionmaker(bind=engine))
    try:
        yield db
    finally:
        db.close()
    transaction.rollback()
    connection.close()
    db.remove()

@pytest.fixture(autouse=True)
def provide_session_to_factories(session):
    # usually you'd have one factory for each db table
    for factory in [UserFactory]:
        factory._meta.sqlalchemy_session = session

def test_persons(session):
    s = session()
    s.add(UserFactory())
    s.add(UserFactory())
    s.commit()

    query_result = s.execute(select(models.DbUser)).all()
    s.close()

    print(query_result[0][0].email)

