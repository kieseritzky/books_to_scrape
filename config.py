#Project Settings
BASE_URL = "https://books.toscrape.com"
HEADLESS = False

#Output Filenames
BASIC_CSV = "books1.csv"
BASIC_JSON = "books1.json"
ADVANCED_CSV = "books2.csv"
ADVANCED_JSON = "books2.json"

#CSV fields mapping to ensure keys match perfectly
BASIC_FIELDS = ["title", "price", "availability", "rating"]
ADVANCED_FIELDS = [
    "description", "upc", "product_type", "price_excl_tax", 
    "price_incl_tax", "tax", "availability", "number_of_reviews"
]
