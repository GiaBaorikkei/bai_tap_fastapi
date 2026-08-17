from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import get_all_products, get_product_detail, delete_product, add_product, update_product
from database import get_db
from schema import ProductCreate

#Tạo các API

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

# Viết API lấy tất cả sản phẩm
@router.get("")
def get_products(db: Session=Depends(get_db)):
    return get_all_products(db)

# Lấy chi tiết sản phẩm
@router.get("/{product_id}")
def get_product_by_id(product_id: int, db: Session=Depends(get_db)):
    return get_product_detail(product_id, db)

@router.delete("/{product_id}")
def delete_product_by_id(product_id: int, db: Session=Depends(get_db)):
    return delete_product(product_id, db)

@router.post("")
def create_product(product: ProductCreate, db: Session=Depends(get_db)):
    return add_product(product, db)

@router.put("/{product_id}")
def update_product_by_id(product_id: int, product: ProductCreate, db: Session=Depends(get_db)):
    return update_product(product_id, product, db)