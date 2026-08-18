from pydantic import BaseModel
class CreateStudent(BaseModel):
    name: str
    email: str
    class_id: int