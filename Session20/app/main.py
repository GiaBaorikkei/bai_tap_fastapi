from fastapi import FastAPI
from app.database.database import engine
from app.database.base import Base

# BẮT BUỘC: Import các models để Base metadata nhận diện được các bảng
from app.models.classroom import Classroom
from app.models.student import Student

# Lệnh này sẽ tự động sinh bảng trong MySQL dựa trên các model đã import ở trên
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ... include_router ...