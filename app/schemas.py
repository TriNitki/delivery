from .static import static
from enum import Enum

countries_dict: dict = {
    country["name"]: country["name"] for country in static.countries
}
cities_dict: dict = {
    city["name"]: city["name"] for city in static.cities
}

CountriesEnum = Enum('Countries', countries_dict)
RussianCitiesEnum = Enum('RussianCities', cities_dict)

class Roles(str, Enum):
    admin = "ADMIN"
    moderator = "MODERATOR"
    seller = "SELLER"
    buyer = "BUYER"

class Genders(str, Enum):
    male = "male"
    female = "female"
    
class Currencies(str, Enum):
    rub = "RUB"
    usd = "USD"
    eur = "EUR"