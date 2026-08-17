from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.student import get_students

""" 
VIẾT API lấy dữ  liệu 

"""

router_student = APIRouter(
    prefix= "/students",
    tags= ["Student"]
)
@router_student.get("")
def get_all_student(db:Session= Depends(get_db) ):
    return get_students(db)