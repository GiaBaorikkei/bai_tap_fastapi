from app.models.student import Student

def get_students(db):
    students = db.query(Student).all()
    return {
            "message":"lấy danh sách sinh viên",
            "data"   : students
            }
        