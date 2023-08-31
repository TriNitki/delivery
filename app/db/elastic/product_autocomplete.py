from elasticsearch import Elasticsearch
from sqlalchemy.orm.state import InstanceState

from ..database import get_es_db
from ...schemas.product import Product, ProductAutoComleteSearch
from ..postgres.models import DbProduct

def add_product(product: DbProduct, client: Elasticsearch = get_es_db()):
    document = ProductAutoComleteSearch(
        name = product.name,
        brand = product.brand,
        description = product.description
    )
    
    client.index(index="product_autocomplete", document=document.model_dump())