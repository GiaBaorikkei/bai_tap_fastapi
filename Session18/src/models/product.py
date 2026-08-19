from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.database.base import Base
from sqlalchemy.orm import relationship

class Product (Base):
    __tablename__  = "product"
    id = Column (Integer, primary_key=True, autoincrement=True)
    product_name = Column (String(100), nullable=False)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("category.id"))
    category_abc = relationship("Category", back_populates="abc_product")