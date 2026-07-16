# Viết hàm lấy dữ liệu từ database

# Hàm lấy tất cả sản phẩm
from fastapi import HTTPException
from models import Product, ProductCreate
def get_all_products(db):
    products = db.query(Product).all()
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }
    
# Hàm lấy chi tiết sản phẩm
def get_product_detail(product_id: int, db):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm"
        )
    return {
        "message": "Tìm thấy sản phẩm thành công",
        "data": product
    }
    
# Hàm thêm sản phẩm
def add_product(product: ProductCreate, db):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Thêm sản phẩm thành công",
        "data": new_product
    }    

# Hàm xoá sản phẩm
def delete_product(product_id: int, db):
    product = db.query(Product).filter(Product.id==product_id).first()
    if product is None:
        raise HTTPException (
            status_code= 404,
            detail= "Không tìm thấy sản phẩm để xoá"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "Xoá sản phẩm thành công",
        "data": product
    }



