from fastapi import FastAPI

from bai1.routers.student import router_student
from bai1.routers.enrollment import router_enrollment
from bai1.routers.course import router_course

app = FastAPI()

app.include_router(router_student)
app.include_router(router_enrollment)
app.include_router(router_course)

@app.get("/")
def home():
    return {
        "message": "API đang chạy!"
    }   