from src.models.product import Product
from src.schema.product import CreateProduct
from fastapi import HTTPException
from src.models.category import Category

def get_product(db):
    product = db.query(Product).all()
    return {
        "message": "Lấy tất cả danh sách sản phẩm",
        "data": product
    }
    
def create_product(product:CreateProduct, db):
    new_product = Product (
        product_name = product.product_name,
        price = product.price,
        category_id = product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "Thêm sản phẩm thành công.",
        "data": new_product
    }

def get_product_detail(product_id, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    category = db.query(Category).filter(Category.id == product.category_id).first()
    product.category = category.name
    return {
        "message": "Lấy chi tiết sản phẩm thành công",
        "data": product,
        # "danh mục": category
    }
    
    