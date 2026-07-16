from fastapi import HTTPException
from models import StudentModel

def delete_student_service(student_id: int, db):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy học viên cần xoá"
        )
    db.delete(student)
    db.commit()
    return {
        "message": "Xoá học viên thành công",
        "data": student
    }