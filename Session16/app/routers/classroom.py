from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.classroom import get_classrooms

""" 
VIẾT API lấy dữ  liệu 

"""

router_classrooms = APIRouter(
    prefix= "/classrooms",
    tags= ["Classroom"]
)
@router_classrooms.get("")
def get_all_classroom(db:Session= Depends(get_db) ):
    return get_classrooms(db)