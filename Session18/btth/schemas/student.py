from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    name: str


class CourseResponse(BaseModel):
    id: int
    name: str


class StudentDetailResponse(BaseModel):
    id: int
    full_name: str
    status: str
    department: DepartmentResponse
    courses: list[CourseResponse]