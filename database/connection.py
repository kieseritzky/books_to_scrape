from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg://{settings.database_username}:{settings.database_password}"
                           f"@{settings.database_hostname}/{settings.database_name}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()