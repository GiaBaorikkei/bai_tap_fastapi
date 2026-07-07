"""
Phân tích
API 1: GET /health

Input

Không có dữ liệu đầu vào.

Output

Trả về thông báo API đang hoạt động.
{
    "message": "API is running"
}

Các bước xử lý

Client gửi request GET /health.
FastAPI gọi endpoint tương ứng.
Trả về thông báo "API is running".
API 2: GET /courses

Input

Không có dữ liệu đầu vào.

Output

Trả về toàn bộ danh sách khóa học.

Các bước xử lý

Client gửi request GET /courses.
FastAPI gọi endpoint.
Trả về danh sách courses.
API 3: GET /courses/{course_id}

Input

course_id (ID của khóa học).

Output

Nếu tìm thấy: trả về thông tin khóa học.
Nếu không tìm thấy: trả về lỗi 404 Not Found.
Nếu course_id <= 0: trả về lỗi phù hợp (400 Bad Request).

Các bước xử lý

Client gửi request GET /courses/{course_id}.
Kiểm tra course_id có hợp lệ hay không.
Duyệt danh sách courses để tìm khóa học có id tương ứng.
Nếu tìm thấy thì trả về thông tin khóa học.
Nếu không tìm thấy thì trả về lỗi 404.
"""

from fastapi import FastAPI

app = FastAPI()

courses = [
    {
        "id": 1,
        "code": "PY101",
        "name": "Python Basic",
        "level": "beginner",
        "price": 1500000
    },
    {
        "id": 2,
        "code": "FA101",
        "name": "FastAPI Basic",
        "level": "beginner",
        "price": 2000000
    }
]

@app.get("/health")
def health():
    return {
        "message": "API is running"
    }

@app.get("/courses")
def get_courses():
    return courses

@app.get("/courses/{course_id}")
def get_course(course_id: int):

    if course_id <= 0:
        return {
            "message": "course_id phải lớn hơn 0"
        }

    for course in courses:
        if course["id"] == course_id:
            return course

    return {
        "message": "Không tìm thấy khóa học"
    }