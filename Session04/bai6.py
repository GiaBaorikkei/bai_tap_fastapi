"""
Phần 1: Phân tích yêu cầu
1. Phân tích Input / Output

Input:

API POST /students/register nhận dữ liệu từ Request Body dạng JSON gồm các trường:

full_name
email
age
phone
course
note (không bắt buộc)

Output:

Thành công: Trả về thông báo đăng ký thành công và thông tin học viên.
Thất bại: Trả về lỗi validate nếu dữ liệu không hợp lệ (thiếu email, email sai định dạng, tuổi ngoài khoảng 15–60, số điện thoại không đúng định dạng, note quá 200 ký tự).
2. Đề xuất 2 giải pháp
Giải pháp 1: Kiểm tra thủ công
Nhận dữ liệu bằng dict.
Dùng if để kiểm tra từng trường.

Ưu điểm: Dễ hiểu.

Nhược điểm: Viết nhiều code, khó bảo trì.

Giải pháp 2: Sử dụng Pydantic BaseModel
Khai báo model bằng BaseModel.
Sử dụng Field và EmailStr để tự động validate dữ liệu.

Ưu điểm: Code ngắn gọn, dễ đọc, ít lỗi.

Nhược điểm: Cần biết cách sử dụng Pydantic.

Phần 2: So sánh và lựa chọn
Tiêu chí	        Giải pháp 1	        Giải pháp 2
Độ dễ hiểu	        Dễ	                Dễ
Số lượng code	    Nhiều	            Ít
Kiểm soát lỗi	    Trung bình	        Tốt
Cấu trúc dữ liệu	Chưa rõ ràng	    Rõ ràng
Lựa chọn

Em chọn Giải pháp 2 (Pydantic BaseModel) vì giúp kiểm tra dữ liệu tự động, giảm số lượng code, dễ đọc và phù hợp với FastAPI. Đây cũng là cách được khuyến khích sử dụng khi xây dựng API.
"""

from fastapi import FastAPI

app = FastAPI()

courses = [
    {
        "id": 1,
        "name": "Python Basic",
        "category": "backend",
        "price": 3000000,
        "mode": "online"
    },
    {
        "id": 2,
        "name": "Java Web",
        "category": "backend",
        "price": 5000000,
        "mode": "offline"
    },
    {
        "id": 3,
        "name": "Web Frontend",
        "category": "frontend",
        "price": 4000000,
        "mode": "online"
    }
]


@app.get("/courses")
def get_courses():
    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": courses
    }


@app.get("/courses/search")
def search_courses(mode: str = None, category: str = None):

    result = courses

    if mode:
        result = [course for course in result if course["mode"] == mode]

    if category:
        result = [course for course in result if course["category"] == category]

    return {
        "message": "Danh sách khóa học",
        "data": result
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):

    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Tìm thấy khóa học",
                "data": course
            }

    return {
        "message": "Không tìm thấy khóa học"
    }