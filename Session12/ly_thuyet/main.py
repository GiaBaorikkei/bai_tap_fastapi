"""
    VIẾT CÁC API
    
    1. Test API trước
    2. Tạo file chưa cấu hính database
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Product, ProductCreate
from services import get_all_products, get_product_detail, delete_product, add_product

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }
    
# API lấy tất cả sản phẩm
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)

#API lấy chi tiết sản phẩm
@app.get("/products/{product_id}")
def get_product_by_id(product_id:int, db: Session=Depends(get_db)):
    return get_product_detail(product_id, db)


# Hàm thêm sản phẩm
@app.post("/products")
def add_detail_product(product: ProductCreate, db: Session = Depends(get_db)):
    return add_product(product, db)
    
# Hàm xoá sản phẩm
@app.delete("/products/{product_id}")
def delete_product_by_id(product_id: int, db: Session= Depends(get_db)):
    return delete_product(product_id, db)

    