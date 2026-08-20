from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from src.schemas.classroom import ClassroomOut # Import từ schema class (cần tạo thêm)

class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    classroom: Optional[ClassroomOut] = None
    model_config = {"from_attributes": True}