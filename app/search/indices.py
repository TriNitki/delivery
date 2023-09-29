from elasticsearch import Elasticsearch, BadRequestError

def create_product_autocomplete_index(client: Elasticsearch):
    try:
        client.indices.create(index='product_autocomplete', mappings={
            "properties": {
                "brand": {"type": "text","fields": {
                    "keyword": {"type": "keyword","ignore_above": 256}}
                },
                "description": {"type": "text","fields": {
                    "keyword": {"type": "keyword","ignore_above": 256}}
                },
                "name": {"type": "text","fields": {
                    "keyword": {"type": "keyword","ignore_above": 256}}
                },
                "id": {"type": "text","fields": {
                    "keyword": {"type": "keyword","ignore_above": 256}}
                },
                "suggest": {"type": "completion"}
                }
            })
        print("product_autocomplete: index was created")
    except BadRequestError:
        print("product_autocomplete: index already exists")

def create_country_autocomplete_index(client: Elasticsearch):
    try:
        client.indices.create(index='country_autocomplete', mappings={
            "properties": {
                "country": {"type": "completion"}
                }
            })
        from ..static import static
        
        for country in static.countries:
            client.index(index="country_autocomplete", document={
                'country': {
                    'input': [country["name"]],
                    'weight': country["population"]
                }})
        print("country_autocomplete: index was created")
    except BadRequestError:
        print("country_autocomplete: index already exists")

def create_city_autocomplete_index(client: Elasticsearch):
    try:
        client.indices.create(index='city_autocomplete', mappings={
            "properties": {
                "city": {"type": "completion"}
                }
            })
        from ..static import static
        
        for city in static.cities:
            client.index(index="city_autocomplete", document={
                'city': {
                    'input': [city["name"]],
                    'weight': city["population"]
                }})
        print("city_autocomplete: index was created")
    except BadRequestError:
        print("city_autocomplete: index already exists")
        

def create_all_indices(client: Elasticsearch):
    create_product_autocomplete_index(client)
    create_country_autocomplete_index(client)
    create_city_autocomplete_index(client)