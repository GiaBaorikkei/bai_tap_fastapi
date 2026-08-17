from app.models.classroom import ClassRoom

def get_classrooms(db):
    classrooms = db.query(ClassRoom).all()
    return {
            "message":"lấy danh sách lớp học thành công",
            "data"   : classrooms
            }
        