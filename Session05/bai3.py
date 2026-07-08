"""
Phần 1: Phân tích và thiết kế giải pháp
1. Phân tích bài toán
Input

API POST /registrations nhận dữ liệu từ Request Body gồm:

student_id
course_id
Output

Thành công:

Tạo phiếu đăng ký mới.
Trả về thông báo đăng ký thành công.
HTTP Status Code: 201 Created.

Thất bại:

student_id không tồn tại.
course_id không tồn tại.
Học viên đã đăng ký khóa học.
Khóa học đã đủ sĩ số.
2. Đề xuất giải pháp
Kiểm tra student_id có tồn tại trong danh sách students.
Kiểm tra course_id có tồn tại trong danh sách courses.
Kiểm tra học viên đã đăng ký khóa học hay chưa.
Đếm số lượng học viên đã đăng ký khóa học.
Nếu số lượng đăng ký bằng capacity thì không cho đăng ký.
Nếu tất cả điều kiện đều hợp lệ thì tạo phiếu đăng ký mới.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]


class Registration(BaseModel):
    student_id: int
    course_id: int


@app.post("/registrations", status_code=201)
def create_registration(registration: Registration):

    # Kiểm tra học viên
    student_found = False
    for student in students:
        if student["id"] == registration.student_id:
            student_found = True

    if not student_found:
        return {
            "detail": "Student not found"
        }

    # Kiểm tra khóa học
    course_found = False
    capacity = 0

    for course in courses:
        if course["id"] == registration.course_id:
            course_found = True
            capacity = course["capacity"]

    if not course_found:
        return {
            "detail": "Course not found"
        }

    # Kiểm tra đăng ký trùng
    for item in registrations:
        if item["student_id"] == registration.student_id and item["course_id"] == registration.course_id:
            return {
                "detail": "Student already registered this course"
            }

    # Kiểm tra sĩ số
    count = 0
    for item in registrations:
        if item["course_id"] == registration.course_id:
            count += 1

    if count >= capacity:
        return {
            "detail": "Course is full"
        }

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Registration successfully",
        "data": new_registration
    }