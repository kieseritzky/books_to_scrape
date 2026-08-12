from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}/"
    "test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = test_engine,
)
