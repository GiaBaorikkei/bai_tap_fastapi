from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bai1.database.database import get_db
from bai1.models.student import Student
from bai1.models.course import Course
from bai1.models.enrollment import Enrollment
from bai1.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse
)


router_enrollment = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router_enrollment.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    data: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    # =====================================
    # 1. Kiểm tra Student tồn tại
    # =====================================

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )


    # =====================================
    # 2. Kiểm tra Course tồn tại
    # =====================================

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )


    # =====================================
    # 3. Kiểm tra Student ACTIVE
    # =====================================

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên không ở trạng thái ACTIVE"
        )


    # =====================================
    # 4. Kiểm tra Course OPEN
    # =====================================

    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đóng"
        )


    # =====================================
    # 5. Kiểm tra đăng ký trùng
    # =====================================

    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học này"
        )


    # =====================================
    # 6. Kiểm tra số lượng sinh viên
    # =====================================

    current_students = db.query(Enrollment).filter(
        Enrollment.course_id == data.course_id,
        Enrollment.status.in_(
            ["STUDYING", "COMPLETED"]
        )
    ).count()

    if current_students >= course.max_students:
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đủ số lượng sinh viên"
        )


    # =====================================
    # 7. Tạo Enrollment
    # =====================================

    new_enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id,
        enrolled_at=datetime.now(),
        status="STUDYING"
    )

    db.add(new_enrollment)

    db.commit()

    db.refresh(new_enrollment)


    # =====================================
    # 8. Trả kết quả
    # =====================================

    return new_enrollment

@router_enrollment.get(
    "/students/{student_id}/courses"
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Kiểm tra sinh viên

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )


    # JOIN Course và Enrollment

    courses = (
        db.query(Course)
        .join(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.status.in_(
                ["STUDYING", "COMPLETED"]
            )
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