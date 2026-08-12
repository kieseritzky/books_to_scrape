from pydantic import BaseModel

class BasicDataOut(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: str

class AdvancedDataOut(BaseModel):
    id: int
    desription: str
    upc: str
    product_type: str
    price_excl_tax: float
    price_inc_tax: float
    tax: float
    availability: str
    number_of_reviews: int