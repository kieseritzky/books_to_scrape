from database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column

class BasicData(Base):
    __tablename__ = "basic_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[float]
    availability: Mapped[str]
    rating: Mapped[str]

class AdvancedData(Base):
    __tablename__ = "advanced_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    upc: Mapped[str]
    product_type: Mapped[str]
    price_excl_tax: Mapped[float]
    price_incl_tax: Mapped[float]
    tax: Mapped[float]
    availability: Mapped[str]
    number_of_reviews: Mapped[int]
