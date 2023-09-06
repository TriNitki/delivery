import json

class Static:
    def __init__(self) -> None:
        with open(r'app/static/countries.json', encoding='utf-8') as f:
            self.countries_dict = {country["name"]: country["name"] for country in json.load(f)}
        with open(r'app/static/russia.json', encoding='utf-8') as f:
            self.cities_dict = {city["city"]: city["city"] for city in json.load(f)}
            

static = Static()