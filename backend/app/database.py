from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.ANALYTICS_DB_USER}:{settings.ANALYTICS_DB_PASSWORD}@{settings.ANALYTICS_DB_HOST}:{settings.ANALYTICS_DB_PORT}/{settings.ANALYTICS_DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
