from app.database.base import Base
from sqlalchemy import Column, Integer, String

class ClassRoom (Base):
    __tablename__ = "classrooms",
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(100), nullable=False)