from pydantic import BaseModel


class StudentCourseItem(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True


class CourseStudentsResponse(BaseModel):
    course_id: int
    course_name: str
    total_students: int
    students: list[StudentCourseItem]