from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base

class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(String(20), unique=True, index=True)
    class_name = Column(String(100))
    max_students = Column(Integer)
    status = Column(String(20), default="active") # active, inactive
    
    # Mối quan hệ 1-N: Trỏ ngược lại bảng students
    # Sử dụng chuỗi "Student" để tránh lỗi circular import
    students = relationship("Student", back_populates="classroom")