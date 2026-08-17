"""
    QUAN HỆ CÁC BẢNG DỮ LIỆU TRONG MYSQL
    
    1. CÁC LOẠI QUAN HỆ TRONG MYSQL
        3 kiểu:
            quan hệ 1-1:
            + 1 sinh viên có 1 hồ sơ
            + 1 cty có 1 giám đốc
            
            quan hệ 1-N
            + Lớp học - Sinh viên (1-N)
            + 1 danh mục có bao nhiều sản phẩm nhưng 1 sản phẩm chỉ thuộc về 1 danh mục
            
            quan hệ N-N
            + môn học - sinh viên
            1 môn học có nhiều sinh viên tham gia học và 1 sinh viên có thể đăng ký nhiều môn học
            
    2. BIỂU DIỄN ĐƯỢC CÁC BẢNG QUAN HỆ TRONG CSDL MYSQL
    
    3. FASTAPI (SQLALCHEMY): thao tác dữ liệu nhanh chóng nhờ các mối quan hệ
"""

from fastapi import FastAPI
from app.routers.classroom import router_classrooms
from app.routers.student import router_student

app = FastAPI()

app.include_router(router_classrooms)
app.include_router(router_student)

@app.get("/")
def home():
    return {
        "message":"API đang chạy!"
    }