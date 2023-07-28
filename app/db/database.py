import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from cassandra.cqlengine.connection import register_connection, set_default_connection
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Postgres config
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:popmenlal@db:5432/delivery"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_pg_db():
    """
    Returns the session generator for the `Postgres` database
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cassandra config

KEYSPACE = os.environ["CASSANDRA_KEYSPACE"]

auth_provider = PlainTextAuthProvider(username='cassandra', password='password')

cluster = Cluster([os.environ["CASSANDRA_IP_ADDRESS"]], port=9042, auth_provider=auth_provider)


def get_ac_db():
    """
    Returns the session generator for the `Apache Cassandra` database
    """
    
    session = cluster.connect()
    return session

_session = get_ac_db()
_session.execute("CREATE KEYSPACE IF NOT EXISTS delivery WITH REPLICATION = "
                "{ 'class' : 'SimpleStrategy', 'replication_factor' : 2 };")

register_connection(str(_session), session=_session)
set_default_connection(str(_session))