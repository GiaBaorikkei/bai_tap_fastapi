"""
Phân tích

1. Input của bài toán là gì?

Danh sách students gồm các sinh viên với các thông tin: id, name, status.

2. Output mong muốn là gì?

API trả về danh sách các sinh viên có status = "active" theo định dạng JSON gồm message và data.

Nếu không có sinh viên đang học thì trả về:

{
    "message": "Không có sinh viên đang học",
    "data": []
}

3. Điều kiện nào dùng để xác định sinh viên đang học?

Sinh viên có status == "active" được xem là đang học.

4. Các bước xử lý API GET /students/active

Client gửi request GET /students/active.
FastAPI tìm endpoint tương ứng.
Duyệt danh sách students.
Lọc các sinh viên có status = "active".
Nếu có dữ liệu thì trả về message và danh sách sinh viên.
Nếu không có dữ liệu thì trả về message thông báo và data là mảng rỗng.
"""

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_active_students():
    active_students = [
        student for student in students
        if student["status"] == "active"
    ]

    if not active_students:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }