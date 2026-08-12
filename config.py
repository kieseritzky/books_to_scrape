from pydantic_settings import BaseSettings, SettingsConfigDict
#Project Settings
BASE_URL = "https://books.toscrape.com"
HEADLESS = True

#Output Filenames
BASIC_CSV = "data/books1.csv"
BASIC_JSON = "data/books1.json"
ADVANCED_CSV = "data/books2.csv"
ADVANCED_JSON = "data/books2.json"

#CSV fields mapping to ensure keys match perfectly
BASIC_FIELDS = ["title", "price", "availability", "rating"]
ADVANCED_FIELDS = [
    "description", "upc", "product_type", "price_excl_tax", 
    "price_incl_tax", "tax", "availability", "number_of_reviews"
]

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore
