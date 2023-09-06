from elasticsearch import Elasticsearch

from ..database import get_es_db

def add_cities(client: Elasticsearch = get_es_db()):
    pass