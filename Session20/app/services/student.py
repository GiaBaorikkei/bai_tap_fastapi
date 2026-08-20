from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.student import Student
from src.models.classroom import Classroom
from src.schema.student import StudentCreate

def create_student_service(db: Session, student_data: StudentCreate):
    # 1. Logic kiểm tra trùng mã SV / Email
    if db.query(Student).filter(Student.student_code == student_data.student_code).first():
        raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại")
        
    # 2. Logic kiểm tra lớp học
    classroom = db.query(Classroom).filter(Classroom.id == student_data.class_id).first()
    if not classroom or classroom.status != "active":
        raise HTTPException(status_code=400, detail="Lớp học không hợp lệ")
        
    # 3. Insert vào DB
    new_student = Student(**student_data.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student