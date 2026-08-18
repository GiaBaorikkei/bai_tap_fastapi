from fastapi import FastAPI
from src.routers.classroom import router_classroom
from src.routers.student import router_student

app = FastAPI()
app.include_router(router_classroom)
app.include_router(router_student)
@app.get("/")
def home():
    return {
        "message": "API đang chạy!"
    }   