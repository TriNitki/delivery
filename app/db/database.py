import os

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from cassandra.cqlengine.connection import register_connection, set_default_connection
from cassandra.cluster import Cluster

import redis

from elasticsearch import Elasticsearch, BadRequestError

from ..config import settings
 
# Postgres implementation
SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_pg_db():
    """
    Returns the session for the `Postgres` database
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cassandra implementation
cluster = Cluster([settings.CASSANDRA_IP_ADDRESS], port=9042)

def get_ac_db():
    """
    Returns the session for the `Apache Cassandra` database
    """
    
    session = cluster.connect()
    return session

_session = get_ac_db()
_session.execute(f"CREATE KEYSPACE IF NOT EXISTS {settings.CASSANDRA_KEYSPACE} WITH REPLICATION = "
                "{ 'class' : 'SimpleStrategy', 'replication_factor' : 2 };")

register_connection(str(_session), session=_session)
set_default_connection(str(_session))

# Redis implementation
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, 
                           password=settings.REDIS_PASSWORD, decode_responses=True)

def get_rds_db():
    """
    Returns the session for the `Redis` database
    """
    
    return redis_client

# Elastic implementation
elastic_client = Elasticsearch(hosts=[f'{settings.WEB_DOMAIN}:{settings.ELASTIC_PORT}'])

try:
    elastic_client.indices.create(index='product_auto_complete', body={
        "mappings": {
            "properties": {
                "brand": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "description": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "name": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "suggest": {"type": "completion"}
                }
            }
        })
except BadRequestError:
    print("product_auto_complete: index already exists")

def get_es_db():
    """
    Returns the session for the `Elastic search` database
    """
    
    return elastic_client