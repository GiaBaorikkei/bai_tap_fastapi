from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from btth.database.database import get_db

from btth.models.student import Student
from btth.models.department import Department
from btth.models.enrollment import Enrollment
from btth.models.course import Course

from btth.schemas.student import StudentDetailResponse


router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router_student.get(
    "/{student_id}",
    response_model=StudentDetailResponse
)
def get_student_detail(
    student_id: int,
    db: Session = Depends(get_db)
):

    # 1. Tìm sinh viên

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )


    # 2. Tìm phòng ban

    department = db.query(Department).filter(
        Department.id == student.department_id
    ).first()


    # 3. Tìm danh sách enrollment

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()


    # 4. Từ enrollment lấy Course

    courses = []

    for enrollment in enrollments:

        course = db.query(Course).filter(
            Course.id == enrollment.course_id
        ).first()

        if course:
            courses.append(course)


    # 5. Trả kết quả

    return {
        "id": student.id,
        "full_name": student.full_name,
        "status": student.status,

        "department": {
            "id": department.id,
            "name": department.name
        },

        "courses": [
            {
                "id": course.id,
                "name": course.name
            }
            for course in courses
        ]
    }