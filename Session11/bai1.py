from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from datetime import datetime

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


# Model
class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


# Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic
class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(..., min_length=3)
    max_weight: int = Field(..., gt=0)


# Hàm Response chuẩn
def response(statusCode, message, error, data, path):
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat()
    }


# API Test
@app.get("/")
def home():
    return {"message": "API đang chạy"}


# POST /parking-slots
@app.post("/parking-slots", status_code=status.HTTP_201_CREATED)
def create_slot(
    slot: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        new_slot = ParkingSlot(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            str(request.url.path)
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Mã vị trí đỗ đã tồn tại"
        )


# GET /parking-slots
@app.get("/parking-slots")
def get_all_slots(
    request: Request,
    db: Session = Depends(get_db)
):
    slots = db.query(ParkingSlot).all()

    data = [
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        }
        for slot in slots
    ]

    return response(
        200,
        "Lấy danh sách vị trí đỗ xe thành công",
        None,
        data,
        str(request.url.path)
    )


# GET /parking-slots/{slot_id}
@app.get("/parking-slots/{slot_id}")
def get_slot(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id
    ).first()

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return response(
        200,
        "Lấy thông tin vị trí đỗ xe thành công",
        None,
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        str(request.url.path)
    )