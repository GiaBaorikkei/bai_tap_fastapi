from sqlalchemy import Column, Integer, String
from src.database.base import Base
from sqlalchemy.orm import relationship

class Category (Base):
    __tablename__  = "category"
    id = Column (Integer, primary_key=True, autoincrement=True)
    name = Column (String(100), nullable=False)
    abc_product = relationship("Product", back_populates="category_abc")