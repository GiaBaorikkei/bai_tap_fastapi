from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from models import Student, Enrollment 
from sqlalchemy.orm import Session
from database import get_db

from schemas import (EnrollmentCreate, EnrollmentResponse, StudentCoursesResponse)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API"
)

@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db)):
    enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment

@app.get("/students/{student_id}/courses", response_model=StudentCoursesResponse, status_code=status.HTTP_200_OK)
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": student.courses
    }