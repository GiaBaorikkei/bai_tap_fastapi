from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

app = FastAPI()

# Kết nối MySQL
DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/connect_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Model Shipment
class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")


# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)


# Dependency Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic Model
class ShipmentCreate(BaseModel):
    tracking_number: str


# API Test
@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }


# Chức năng 1: Đăng ký mã vận đơn mới
@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(
    shipment: ShipmentCreate,
    db: Session = Depends(get_db)
):
    # Kiểm tra mã vận đơn đã tồn tại chưa
    existed = db.query(ShipmentModel).filter(
        ShipmentModel.tracking_number == shipment.tracking_number
    ).first()

    if existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vận đơn này đã được khởi tạo trước đó"
        )

    new_shipment = ShipmentModel(
        tracking_number=shipment.tracking_number
    )

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    return {
        "message": "Đăng ký mã vận đơn thành công",
        "data": new_shipment
    }


# Chức năng 2: Lấy danh sách tất cả mã vận đơn
@app.get("/shipments", status_code=status.HTTP_200_OK)
def get_all_shipments(
    db: Session = Depends(get_db)
):
    shipments = db.query(ShipmentModel).all()

    return {
        "message": "Lấy danh sách mã vận đơn thành công",
        "data": shipments
    }