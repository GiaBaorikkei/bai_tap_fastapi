from app.database.base import Base
from sqlalchemy import Column, Integer, String

class Student (Base):
    __tablename__ = "students",
    
    id = Column(Integer, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    class_id = Column(Integer)
    
    
    