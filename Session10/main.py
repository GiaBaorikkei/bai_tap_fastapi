from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

app = FastAPI()

# Địa chỉ của CSDL MySQL
DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/connect_db"

# Tạo engine kết nối đến MySQL
engine = create_engine(DATABASE_URL)

# Tạo Session
SessionLocal = sessionmaker(bind=engine)

# Tạo Base để khai báo Model
Base = declarative_base()


# Tạo bảng Product
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)


# Tạo bảng trong MySQL nếu chưa tồn tại
Base.metadata.create_all(bind=engine)


# Tạo phiên làm việc với database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API test
@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }


# API lấy tất cả sản phẩm
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    }

# API lấy chi tiết sản phẩm
@app.get("/products/{product_id}")
def get_product_detail(product_id: int, db: Session= Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException (
            status_code = 404,
            detail="Không tìm thấy sản phẩm"
        )
    return {
        "message": "Lấy chi tiết sản phẩm thành công",
        "data": product
    }
    
#API thêm sản phẩm
class ProductCreate(BaseModel):
    name: str
    price: float

@app.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
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

#API Xoá sản phẩm
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session= Depends(get_db)):
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
    
#Cập nhật sản phẩm
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    update_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sản phẩm cần cập nhật"
        )

    product.name = update_product.name
    product.price = update_product.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Cập nhật sản phẩm thành công",
        "data": product
    }
    
    
    