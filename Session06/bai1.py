from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class CreateRequest(BaseModel):
    id: int
    code: str
    name: str
    duration: int = Field(gt=0)
    fee: int = Field(ge=0)
    

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

# Thêm khoá học
@app.post("/courses")
def create_courses(course: CreateRequest):
    for c in courses:
        if c["code"] == course.code:
            return "Code không được trùng."
    if course.name == "":
        return "Tên không được để trống."
    
    new_course = course.model_dump()
    
    courses.append(new_course)
    
    return {
        "message": "Thêm khoá học thành công",
        "data": new_course
    }
    
# Lấy danh sách khoá học
@app.get("/courses")
def get_courses():
    return courses

# Lấy chi tiết khoá học
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for c in courses:
        if c["id"] == course_id:
            return c
    return "Không tìm thấy khoá học"

# Cập nhật khoá học
@app.put("/courses/{course_id}")
def update_course(course_id: int, request: CreateRequest):
    for course in courses:
        if course["id"] == course_id:
            for c in courses:
                if c["code"] == request.code and c["id"] != course_id:
                    return "Code đã tồn tại."
            if request.name.strip() == "":
                return "Tên không được để trống."
            course.update(request.model_dump())
            
            return {
                "message": "Cập nhật khoá học thành công",
                "data": course
            }
    return "Không tìm thấy khoá học"

# Xoá khoá học
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return "Xoá thành công"
        
    return "Không tìm thấy khoá học"

