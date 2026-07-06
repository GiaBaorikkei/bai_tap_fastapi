from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Bảo"},
    {"id": 2, "name": "Huyền"}
]

@app.get("/students")
def home():
    return {"message": "Hello Gia Bảo"}

@app.get("/students/{student_id}", summary = "Lấy ra thông tin chi tiết sinh viên")
def getStudent(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student