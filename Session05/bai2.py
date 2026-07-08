"""
Phần 1: Chỉ ra lỗi bằng test case
STT	Dữ liệu gửi lên	                        Kết quả hiện tại	Kết quả đúng mong muốn	                    Lỗi phát hiện
1	student_id = "SV001", course_id = 1	    Vẫn đăng ký được	Báo lỗi học viên đã đăng ký khóa học này	Không kiểm tra đăng ký trùng
2	student_id = "SV002", course_id = 1	    Vẫn đăng ký được	Báo lỗi học viên đã đăng ký khóa học này	Cho phép đăng ký trùng

Kết luận: API chưa kiểm tra xem học viên đã đăng ký khóa học đó hay chưa nên có thể tạo nhiều bản ghi trùng.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]


class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int


@app.post("/enrollments", status_code=201)
def create_enrollment(enrollment: EnrollmentCreate):

    for e in enrollments:
        if e["student_id"] == enrollment.student_id and e["course_id"] == enrollment.course_id:
            return {
                "message": "Học viên đã đăng ký khóa học này"
            }

    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }