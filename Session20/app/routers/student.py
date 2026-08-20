from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schema import student as student_schema
from src.services import student as student_service
# Chú ý: Cần import hàm create_response từ file tiện ích của bạn

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", status_code=201)
def create_student_api(
    student: student_schema.StudentCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    # Ủy quyền toàn bộ logic cho tầng Service
    new_student = student_service.create_student_service(db, student)
    
    # Trả về format chuẩn
    return create_response(request, 201, "Thêm sinh viên thành công", new_student)