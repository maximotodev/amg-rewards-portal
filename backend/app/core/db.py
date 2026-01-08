from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

class Base(DeclarativeBase):
    pass

# We use the DATABASE_URL from our config
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# This is the function the error said was missing:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
