from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
import logging

logger = logging.getLogger("gunicorn.error")

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("*"*25)
logger.info(f"DATABASE URL - {SQLALCHEMY_DATABASE_URL}")
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
