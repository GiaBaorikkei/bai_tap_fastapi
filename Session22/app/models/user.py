from sqlalchemy import Column, Integer, String
from app.database.base import Base

class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(550), nullable=False)
    
    