from elasticsearch import Elasticsearch

from ..database import get_es_db

def autocomplete(text: str, client: Elasticsearch = get_es_db()):
    suggest_dictionary = {"suggests" : {
        "prefix": text,
        "completion" : {
            "field" : "city",
            "skip_duplicates": True
            }
        }
    }
    
    query_dictionary = {
        'suggest' : suggest_dictionary
        }
    res = client.search(
        index='city_autocomplete',
        body=query_dictionary
    )
    
    options = [
        option['text'] for option in res.body['suggest']['suggests'][0]['options']
    ]
    return options