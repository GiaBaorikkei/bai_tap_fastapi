from fastapi import FastAPI

app = FastAPI()


@app.get("/students")
def get_students():
    return {
        "message": "Lấy danh sách sinh viên thành công"
    }


@app.get("/students/detail")
def get_student_detail():
    return {
        "message": "Thông tin chi tiết sinh viên"
    }

@app.post("/students")
def add_student():
    return {
        "message": "Thêm sinh viên thành công"
    }


@app.put("/students/update")
def update_student():
    return {
        "message": "Cập nhật sinh viên thành công"
    }


@app.delete("/students/delete")
def delete_student():
    return {
        "message": "Xóa sinh viên thành công"
    }


@app.get("/students/statistics")
def statistics_student():
    return {
        "message": "Thống kê sinh viên"
    }


@app.get("/students/active")
def active_students():
    return {
        "message": "Danh sách sinh viên đang học"
    }


@app.get("/students/top")
def top_students():
    return {
        "message": "Danh sách sinh viên xuất sắc"
    }