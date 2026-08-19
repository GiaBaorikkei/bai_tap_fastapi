from fastapi import FastAPI

from btth.routers.student import router_student
from btth.routers.enrollment import router_enrollment


app = FastAPI()


app.include_router(
    router_student
)

app.include_router(
    router_enrollment
)


@app.get("/")
def root():
    return {
        "message": "API quản lý sinh viên và khóa học"
    }