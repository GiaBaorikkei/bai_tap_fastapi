"""
1. Trace luồng xử lý khi gọi /getStudents

Client gửi request GET /getStudents.
FastAPI tìm route /getStudents.
Gọi hàm get_students().
Hàm lấy dữ liệu từ students.
FastAPI trả response về cho client.

2. Vì sao FastAPI không nên trả về string trong API JSON

API nên trả về dữ liệu JSON để frontend dễ xử lý.
Trả về string khiến frontend chỉ nhận được một chuỗi, không thể đọc như một danh sách JSON.
FastAPI có thể tự chuyển list hoặc dict thành JSON nên không cần nối chuỗi.

3. Lỗi trong thiết kế REST endpoint (Naming Convention)

Endpoint /getStudents chưa đúng chuẩn REST vì chứa động từ get.
Nên đặt tên theo tài nguyên, ví dụ: /students.
HTTP Method GET đã thể hiện hành động lấy dữ liệu nên không cần thêm get vào tên endpoint.
"""

from fastapi import FastAPI

app = FastAPI()

students = ["An", "Bình", "Cuong"]

@app.get("/students")
def get_students():
    return {"Danh sách sinh viên": students}