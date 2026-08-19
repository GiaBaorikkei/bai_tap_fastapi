from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from btth.database.database import get_db

from btth.models.student import Student
from btth.models.course import Course
from btth.models.enrollment import Enrollment

from btth.schemas.enrollment import EnrollmentCreate


router_enrollment = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router_enrollment.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    data: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    # =================================
    # 1. Kiểm tra Student tồn tại
    # =================================

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )


    # =================================
    # 2. Kiểm tra Student ACTIVE
    # =================================

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên không ở trạng thái ACTIVE"
        )


    # =================================
    # 3. Kiểm tra Course tồn tại
    # =================================

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )


    # =================================
    # 4. Kiểm tra Course OPEN
    # =================================

    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Khóa học không ở trạng thái OPEN"
        )


    # =================================
    # 5. Kiểm tra đăng ký trùng
    # =================================

    existing_enrollment = db.query(
        Enrollment
    ).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học này"
        )


    # =================================
    # 6. Tạo Enrollment
    # =================================

    new_enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(new_enrollment)

    db.commit()

    db.refresh(new_enrollment)


    # =================================
    # 7. Trả kết quả
    # =================================

    return {
        "id": new_enrollment.id,
        "student_id": new_enrollment.student_id,
        "course_id": new_enrollment.course_id
    }