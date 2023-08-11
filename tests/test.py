import logging

import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine, select
from sqlalchemy.orm.session import sessionmaker

from ..app.db.postgres import models

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

test_db = factories.postgresql_proc(port=None, dbname="test_db")

@pytest.fixture(scope="session")
def db_session(test_db):
    """Session for SQLAlchemy."""
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_str)
        with engine.connect() as con:
            sql_schema.Base.metadata.create_all(con)
            logger.info("yielding a sessionmaker against the test postgres db.")

            yield sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="module")
def create_test_data():
    """Let's create the test data with the three witches names."""
    names = ["Winifred", "Sarah", "Mary"]
    test_objs = []
    for idx, name in zip(range(3), names):
        test_objs.append(sql_schema.Person(ID=idx, Name=name))

    return test_objs


def test_persons(db_session, create_test_data):
    s = db_session()
    for obj in create_test_data:
        s.add(obj)
    s.commit()
    logger.info("Added test data to the database.")

    query_result = s.execute(select(sql_schema.Person)).all()
    s.close()

    assert create_test_data[0].Name in str(query_result)