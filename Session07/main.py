from fastapi import FastAPI, status, HTTPException
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

mock_database = {}

@app.post("/users")
def create_user(user: UserCreate):
    user_id = len(mock_database) + 1
    user_data = user.model_dump()
    user_data["id"] = user_id
    mock_database[user_id] = user_data
    return user_data

@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id not in mock_database:
        raise HTTPException(   
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại."
        )
    return user_id[user_id]