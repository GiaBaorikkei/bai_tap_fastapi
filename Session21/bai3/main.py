from fastapi import FastAPI

from database import Base, engine
from auth_router import router_auth


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Student Management API",
    description="API đăng ký, đăng nhập và xác thực người dùng",
    version="1.0.0"
)


app.include_router(
    router_auth
)


@app.get("/")
def root():
    return {
        "message": "Student Management API"
    }