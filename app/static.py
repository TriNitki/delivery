import json

class Static:
    def __init__(self) -> None:
        with open(r'app/static/country-by-population.json', encoding='utf-8') as f:
            self.countries = [
                {
                    "name": country["country"], 
                    "population": country["population"]
                } for country in json.load(f)
            ]
        with open(r'app/static/russian-cities.json', encoding='utf-8') as f:
            self.cities = [
                {
                    "name": city["name"], 
                    "population": city["population"]
                } for city in json.load(f)
            ]

url_regex = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
static = Static()