"""
Phần 1: Luồng dữ liệu
Client gửi yêu cầu POST /memberships gồm card_number và customer_id.
Hệ thống dùng SELECT (.first()) để kiểm tra customer_id có tồn tại trong bảng customers hay không.
Nếu không tồn tại → raise HTTPException(404) với thông báo "Khách hàng không tồn tại trên hệ thống".
Tiếp tục dùng SELECT (.first()) để kiểm tra card_number đã tồn tại trong bảng memberships hay chưa.
Nếu đã tồn tại → raise HTTPException(400) với thông báo "Mã số thẻ thành viên này đã được sử dụng".
Nếu cả hai điều kiện đều hợp lệ → tạo đối tượng MembershipModel, gọi db.add(), db.commit(), db.refresh() để lưu vào MySQL.
Trả về kết quả thành công 201 Created theo đúng cấu trúc phản hồi quy định.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
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


# Model
class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class MembershipModel(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)


Base.metadata.create_all(bind=engine)


# Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request Model
class MembershipCreate(BaseModel):
    card_number: str
    customer_id: int


# API Test
@app.get("/")
def home():
    return {"message": "API đang chạy"}


# API tạo thẻ thành viên
@app.post("/memberships", status_code=status.HTTP_201_CREATED)
def create_membership(
    membership: MembershipCreate,
    db: Session = Depends(get_db)
):
    # Kiểm tra khách hàng
    customer = db.query(CustomerModel).filter(
        CustomerModel.id == membership.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khách hàng không tồn tại trên hệ thống"
        )

    # Kiểm tra trùng số thẻ
    card = db.query(MembershipModel).filter(
        MembershipModel.card_number == membership.card_number
    ).first()

    if card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã số thẻ thành viên này đã được sử dụng"
        )

    # Thêm mới
    new_membership = MembershipModel(
        card_number=membership.card_number,
        customer_id=membership.customer_id
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)

    return {
        "message": "Đăng ký thẻ thành viên thành công",
        "data": new_membership
    }