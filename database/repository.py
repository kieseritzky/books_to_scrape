from .models import BasicData, AdvancedData
from database.connection import SessionLocal
from sqlalchemy.dialects.postgresql import insert

def basic_save_to_postgres(record):
    with SessionLocal() as db:
        stmt = insert(BasicData).values(**record)
        stmt = stmt.on_conflict_do_nothing(
            index_elements = ["upc"]
        )

        db.execute(stmt)
        db.commit()

def advanced_save_to_postgres(record):
    with SessionLocal() as db:
        stmt = insert(AdvancedData).values(**record)
        stmt = stmt.on_conflict_do_nothing(
            index_elements = ["upc"]
        )
        db.execute(stmt)
        db.commit()
