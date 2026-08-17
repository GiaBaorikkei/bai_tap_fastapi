from models import Product
from schema import ProductCreate
from fastapi import HTTPException

def get_all_products(db):
    products = db.query(Product).all()
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    return {
        "message": "Lấy sản phẩm thành công",
        "data": product
    }

def add_product(product: ProductCreate, db):
    new_product = Product(
        name = product.name,
        price = product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "Thêm sản phẩm thành công!",
        "data": new_product
    }
    
def update_product(product_id: int, product: ProductCreate, db):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    product_db.name = product.name
    product_db.price = product.price
    db.commit()
    db.refresh(product_db)
    return {
        "message": "Cập nhật sản phẩm thành công",
        "data": product_db
    }

def delete_product(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "Xoá sản phẩm thành công",
        "data": product
    }
    