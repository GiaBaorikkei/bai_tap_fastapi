from pydantic import BaseModel

class ClassroomBase(BaseModel):
    class_code: str
    class_name: str
    max_students: int
    status: str = "active"

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomOut(BaseModel):
    id: int
    class_code: str
    class_name: str
    status: str

    model_config = {"from_attributes": True}