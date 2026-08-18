from sqlalchemy import Column, Integer, String
from src.database.base import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    class_id = Column(Integer)
