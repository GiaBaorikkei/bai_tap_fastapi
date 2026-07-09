from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class CreateRequest(BaseModel):
    id: int
    code: str
    name: str
    email: EmailStr
    age: int
    

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

# Thêm học viên    
@app.post("/students")
def create_students(student: CreateRequest):
    for s in students:
        if s["code"] == student.code:
            return "Code không được trùng."
    if student.name.strip() == "":
        return "Tên không được để trống."
    if student.email.strip() == "":
        return "Email không được để trống"
    
    new_student = student.model_dump()
    
    students.append(new_student)
    
    return {
        "message": "Thêm học viên thành công",
        "data": new_student
    }
    
# Lấy danh sách học viên
@app.get("/students")
def get_students():
    return students

# Lấy chi tiết học viên
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    return "Không tìm thấy học viên"

# Cập nhật học viên
@app.put("/students/{student_id}")
def update_student(student_id: int, request: CreateRequest):
    for student in students:
        if student["id"] == student_id:
            for s in students:
                if s["code"] == request.code and s["id"] != student_id:
                    return "Code đã tồn tại."
            if request.name.strip() == "":
                return "Tên không được để trống."
            if request.email.strip() == "":
                return "Email không được để trống"
            
            student.update(request.model_dump())
            
            return {
                "message": "Cập nhật học viên thành công",
                "data": student
            }
    return "Không tìm thấy học viên"

# Xoá học viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return "Xoá thành công"
        
    return "Không tìm thấy học viên"

