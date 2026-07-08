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
Cấu trúc dữ liệu	Chưa rõ ràng	Rõ ràng
Lựa chọn

Em chọn Giải pháp 2 (Pydantic BaseModel) vì giúp kiểm tra dữ liệu tự động, giảm số lượng code, dễ đọc và phù hợp với FastAPI. Đây cũng là cách được khuyến khích sử dụng khi xây dựng API.
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11)
    course: str
    note: str = Field(default="", max_length=200)


@app.post("/students/register")
def register(student: StudentRegister):

    # Kiểm tra số điện thoại chỉ chứa số
    if not student.phone.isdigit():
        return {
            "message": "Số điện thoại chỉ được chứa chữ số"
        }

    return {
        "message": "Đăng ký học viên thành công",
        "data": {
            "full_name": student.full_name.strip(),
            "email": student.email,
            "age": student.age,
            "phone": student.phone,
            "course": student.course,
            "note": student.note.strip()
        }
    }