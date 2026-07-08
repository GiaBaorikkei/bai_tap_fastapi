from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

students = [
    {"id": 1, "name": "Nguyễn Văn An"},
    {"id": 2, "name": "Trần Thị Bình"},
    {"id": 3, "name": "Lê Văn Cường"},
    {"id": 4, "name": "Phạm Thị Dung"}
]

class Student(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=10)

class UpdateStudent(BaseModel):
    name: str 

app = FastAPI()

@app.get("/")
def welcome():
    return "Xin chào tất cả các bạn"

# API lất thông tin chi tiết tất cả sinh viên 
@app.get("/students/{student_id}")
def get_student():
    return "Lấy thông tin chi tiết sinh viên"

# API cập nhật thông tin sinh viên
@app.put("/students/{student_id}")
def update_student(update:UpdateStudent, student_id: int):
    for i in students:
        if i["id"] == student_id:
            i["name"] = update.name
        return students
        