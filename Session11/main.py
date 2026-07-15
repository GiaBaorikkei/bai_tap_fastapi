"""
1. TẠO BẢNG DATABASE: connect_db
2. TẠO BẢNG STUDENTS với các thuộc tính
    + id: mã sinh viên
    + name: tên sinh viên
    + class: tên lớp
    + email: email sinh viên
    
3 Viết các API
    + test API đang chạy
    + API lấy danh sách sinh viên
    + API lấy chi tiết sinh viên theo id
    + API thêm sinh viên
    + API xoá sinh viên
    + API cập nhật sinh viên
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

app = FastAPI()

# Địa chỉ của CSDL MySQL
DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/connect_db"

# Tạo engine kết nối
engine = create_engine(DATABASE_URL)

# Tạo Session
SessionLocal = sessionmaker(bind=engine)

# Tạo Base
Base = declarative_base()

# MODEL
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    class_name = Column("class", String(20), nullable=False)
    email = Column(String(50), nullable=False)


# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

# DATABASE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic Model
class StudentCreate(BaseModel):
    name: str
    class_name: str
    email: str

# API TEST
@app.get("/")
def home():
    return {
        "message": "API đang chạy"
    }

# LẤY DANH SÁCH SINH VIÊN
@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return {
        "message": "Lấy danh sách sinh viên thành công",
        "data": students
    }

# LẤY CHI TIẾT SINH VIÊN
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    return {
        "message": "Lấy chi tiết sinh viên thành công",
        "data": student
    }


# THÊM SINH VIÊN
@app.post("/students")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        class_name=student.class_name,
        email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Thêm sinh viên thành công",
        "data": new_student
    }


# CẬP NHẬT SINH VIÊN
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    update_student: StudentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    student.name = update_student.name
    student.class_name = update_student.class_name
    student.email = update_student.email

    db.commit()
    db.refresh(student)

    return {
        "message": "Cập nhật sinh viên thành công",
        "data": student
    }


# XÓA SINH VIÊN
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Xóa sinh viên thành công"
    }