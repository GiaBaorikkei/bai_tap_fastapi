from fastapi import FastAPI
from app.routers.user import router_user

app = FastAPI()
app.include_router(router_user)

@app.get("/")
def home():
    return {
        "message": "API đang chạy!"
    }   