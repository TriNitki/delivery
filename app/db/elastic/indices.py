from elasticsearch import Elasticsearch, BadRequestError

def create_product_autocomplete_index(client: Elasticsearch):
    try:
        client.indices.create(index='product_autocomplete', mappings={
            "properties": {
                "brand": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "description": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "name": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},
                "suggest": {"type": "completion"}
                }
            })
    except BadRequestError:
        print("product_autocomplete: index already exists")

def create_country_autocomplete_index(client: Elasticsearch):
    try:
        client.indices.create(index='country_autocomplete', mappings={
            "properties": {
                "country": {"type": "completion"}
                }
            })
        from ...utils.static import static
        
        for country in static.countries_dict.values():
            client.index(index="country_autocomplete", document={'country': country})
    except BadRequestError:
        print("country_autocomplete: index already exists")

def create_all_indices(client: Elasticsearch):
    create_product_autocomplete_index(client)
    create_country_autocomplete_index(client)