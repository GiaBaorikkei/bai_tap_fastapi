"""
Phân tích lỗi

1. Endpoint hiện tại trong source code là gì?

Endpoint hiện tại là GET /student.

2. Vì sao khi gọi GET /students lại bị lỗi 404 Not Found?

Vì trong source code không khai báo route /students, nên FastAPI không tìm thấy endpoint tương ứng.

3. Vì sao tên endpoint /student chưa phù hợp với yêu cầu lấy danh sách sinh viên?

/student biểu thị một sinh viên, trong khi yêu cầu là lấy danh sách sinh viên.
Theo chuẩn REST nên dùng /students.

4. Vì sao dòng return students[0] chưa đúng với yêu cầu nghiệp vụ?

students[0] chỉ trả về sinh viên đầu tiên.
Yêu cầu của bài là trả về toàn bộ danh sách sinh viên.

5. API đúng theo yêu cầu khách hàng nên có đường dẫn là gì?

GET /students.
"""

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"}
]

@app.get("/students")
def get_students():
    return students