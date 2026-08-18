from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.students import Student
from src.models.classrooms import Classroom
from src.schemas.student import CreateStudent

router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router_student.get("")
def get_all_student(db:Session = Depends(get_db)):
    students = db.query(Student).all()
    return {
        "message": "Lấy danh sách tất cả sinh viên",
        "data": students
    }

@router_student.get("{student_id}")
def get_student_detail(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if student is None:
        raise HTTPException (
            status_code=404,
            detail="không tìm thấy sinh viên"
        )
    classroom = db.query(Classroom).filter(Classroom.id == student.class_id).first()
    student.class_name = classroom.class_name
    return {
        "message": "Lấy thông tin sinh viên thành công",
        "data": student
    }

@router_student.post("/")
def add_student(request:CreateStudent, db: Session=Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == request.class_id)
    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )
    student = Student(
        name = request.name,
        email = request.email,
        class_id = request.class_id
    )
    
    db.add(student)
    db.commit()
    db.refresh()