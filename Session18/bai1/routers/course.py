from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bai1.database.database import get_db
from bai1.models.course import Course
from bai1.models.student import Student
from bai1.models.enrollment import Enrollment
from bai1.schemas.course import CourseStudentsResponse


router_course = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router_course.get(
    "/{course_id}/students",
    response_model=CourseStudentsResponse
)
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db)
):

    # =====================================
    # 1. Kiểm tra Course tồn tại
    # =====================================

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )


    # =====================================
    # 2. JOIN Student + Enrollment
    # =====================================

    students = (
        db.query(Student)
        .join(
            Enrollment,
            Enrollment.student_id == Student.id
        )
        .filter(
            Enrollment.course_id == course_id,

            Enrollment.status.in_(
                ["STUDYING", "COMPLETED"]
            ),

            Student.status == "ACTIVE"
        )
        .distinct()
        .order_by(
            Student.full_name.asc()
        )
        .all()
    )


    # =====================================
    # 3. Trả kết quả
    # =====================================

    return {
        "course_id": course.id,
        "course_name": course.name,
        "total_students": len(students),
        "students": students
    }