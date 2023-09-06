from ..utils.static import static
from enum import Enum

CountriesEnum = Enum('Countries', static.countries_dict)
RussianCitiesEnum = Enum('RussianCities', static.cities_dict)

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