"""
Phần 1: Phân tích & Đề xuất đa giải pháp
1. Phân tích Input / Output

Input

API nhận request POST /students với dữ liệu JSON gồm:

full_name
email
age
course
phone

Output

Thành công: Trả về thông báo thêm học viên thành công và thông tin học viên.
Thất bại: Trả về thông báo lỗi khi thiếu trường bắt buộc, email sai định dạng hoặc email đã tồn tại.
2. Hai giải pháp

Giải pháp 1: Validate thủ công

Dùng if, for để kiểm tra từng trường dữ liệu.
Ưu điểm: Dễ hiểu.
Nhược điểm: Viết nhiều code.

Giải pháp 2: Dùng Pydantic Model

Sử dụng BaseModel và EmailStr để tự động kiểm tra dữ liệu.
Ưu điểm: Code ngắn gọn, dễ bảo trì.
Nhược điểm: Cần biết cách dùng Pydantic.

Phần 2: So sánh & Lựa chọn
Tiêu chí	        Giải pháp 1	        Giải pháp 2
Độ dễ hiểu	        Dễ	                Dễ
Số lượng code	    Nhiều	            Ít
Kiểm soát lỗi	    Trung bình	        Tốt
Cấu trúc dữ liệu	Chưa rõ             Rõ ràng

Lựa chọn: Em chọn Giải pháp 2 vì code ngắn gọn, dễ đọc, FastAPI hỗ trợ sẵn và dễ mở rộng khi phát triển sau này.

Bản này ngắn gọn khoảng nửa trang A4, phù hợp để nộp bài thực hành.
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

students = []


class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int
    course: str
    phone: str


@app.post("/students")
def add_student(student: Student):

    for s in students:
        if s["email"] == student.email:
            return {
                "detail": "Email đã tồn tại trong hệ thống"
            }

    students.append(student.model_dump())

    return {
        "message": "Thêm học viên thành công",
        "student": student
    }