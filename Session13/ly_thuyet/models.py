from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float

Base = declarative_base()

# Tạo bảng dữ liệu ánh xạ đến bảng trong MySql
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    