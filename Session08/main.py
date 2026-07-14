from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


students = []

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

@app.get("/")
def home():
    return {
        "message": "api đang chạy"
    }
    
@app.get("/students")
def get_students():
    return students

@app.post("/students")
def add_students(new_student: StudentCreate):
    new_id = len(students) + 1
    add_new_student = {
        "id": new_id,
        "name": new_student.name,
        "email": new_student.email
    }
    students.append(add_new_student)
    return add_new_student
    
    
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for std in students:
        if std["id"] == student_id:
            students.remove(std)
            return {
                "message": "Xoá sinh viên thành công.",
                "data": std
            }
    return "không tim thấy sinh viên"

@app.put("/students/{student_id}")
def update_student(student_id:int, update_student: StudentCreate):
    for std in students:
        if std["id"] == student_id:
            std["name"] = update_student.name
            std["email"] = update_student.email
            return {
                "message": "Cập nhật thành công",
                "data": std
            }
    return "Không tìm thấy sinh viên"