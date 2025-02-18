# src/infrastructure/persistence/models.py
from sqlalchemy import Column, Integer, String
from infrastructure.persistence.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, )
    email = Column(String(356), unique=True, index=True)