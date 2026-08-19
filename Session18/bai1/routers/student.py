from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bai1.database.database import get_db
from bai1.models.student import Student
from bai1.models.course import Course
from bai1.models.enrollment import Enrollment


router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router_student.get("/{student_id}/courses")
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    # Tìm sinh viên
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    # JOIN Enrollment với Course
    courses = (
        db.query(Course)
        .join(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .filter(
            Enrollment.student_id == student_id
        )
        .all()
    )

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": [
            {
                "id": course.id,
                "name": course.name
            }
            for course in courses
        ]
    }
    
