from elasticsearch import Elasticsearch

from ..database import get_es_db
from ...schemas.product import ProductAutoComleteSearch, ProductSuggest
from ..postgres.models import DbProduct

def add_product(product: DbProduct, client: Elasticsearch = get_es_db()):
    suggest = ProductSuggest(
        input = [*product.name.split(), product.brand],
        weight = 10
    )
    
    document = ProductAutoComleteSearch(
        name = product.name,
        brand = product.brand,
        description = product.description,
        suggest = suggest
    )
    
    client.index(index="product_autocomplete", document=document.model_dump())
    
def autocomplete(text: str, client: Elasticsearch = get_es_db()):
    request = text.split()
    prefix = request[-1]
    
    suggest_dictionary = {"suggests" : {
        "prefix": prefix,
        "completion" : {
            "field" : "suggest",
            "skip_duplicates": True
            }
        }
    }

    query_dictionary = {'suggest' : suggest_dictionary}
    res = client.search(
        index='product_autocomplete',
        body=query_dictionary
    )
    
    
    options = [
        option['text'] for option in res.body['suggest']['suggests'][0]['options']
    ]
    suggestions = [' '.join(request[:-1] + [option]) for option in options]
    return suggestions