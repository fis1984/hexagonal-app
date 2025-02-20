from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.setting import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

# Metadata para acceder a las tablas
metadata = MetaData()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
