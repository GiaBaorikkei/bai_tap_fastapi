"""
Phần 1: Phân tích Input/Output

Input

API: `GET /shipments/{shipment_id}`
Tham số:`shipment_id`
Kiểu dữ liệu: `int`
Ý nghĩa: ID của mã vận đơn cần tra cứu.

Output thành công (200 OK)

```json
{
    "message": "Lấy thông tin vận đơn thành công",
    "data": {
        "id": 1,
        "tracking_number": "GHTK000001",
        "status": "PREPARING"
    }
}
```

Output thất bại (404 Not Found)

```json
{
    "detail": "Không tìm thấy mã vận đơn"
}
```

---

# Phần 2: So sánh & Lựa chọn giải pháp

| Tiêu chí            | `.all()` + lọc Python | `.filter().first()`            |
| ------------------- | --------------------- | ------------------------------ |
| Dữ liệu lấy lên RAM | Toàn bộ bản ghi       | 1 bản ghi                      |
| SQL                 | `SELECT *`            | `SELECT ... WHERE ... LIMIT 1` |
| Hiệu năng           | Chậm khi dữ liệu lớn  | Nhanh, tối ưu                  |
| Phù hợp             | Lấy toàn bộ dữ liệu   | Tìm một bản ghi                |

Kết luận

Nên sử dụng `.filter().first()`** vì chỉ lấy đúng một bản ghi cần tìm, tiết kiệm RAM, giảm tải cho Database và cho tốc độ xử lý nhanh hơn so với `.all()`.

"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

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


Base.metadata.create_all(bind=engine)


# Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Test
@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }


# API Tra cứu mã vận đơn
@app.get("/shipments/{shipment_id}", status_code=status.HTTP_200_OK)
def get_shipment(
    shipment_id: int,
    db: Session = Depends(get_db)
):
    shipment = (
        db.query(ShipmentModel)
        .filter(ShipmentModel.id == shipment_id)
        .first()
    )

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy mã vận đơn"
        )

    return {
        "message": "Lấy thông tin vận đơn thành công",
        "data": shipment
    }