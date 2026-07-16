from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import delete_student_service

app = FastAPI()

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session= Depends(get_db)):
    return delete_student_service(student_id, db)
