from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import redis

from elasticsearch import Elasticsearch

from .search import indices
from .config import settings
 
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

indices.create_all_indices(elastic_client)

def get_es_db():
    """
    Returns the session for the `Elastic search` database
    """
    
    return elastic_client