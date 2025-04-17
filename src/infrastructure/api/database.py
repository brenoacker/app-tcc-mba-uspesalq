from sqlalchemy import create_engine
# Update this import to use the new location
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

engine = create_engine(settings.CONNECTION)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the imported declarative_base from sqlalchemy.orm
Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)