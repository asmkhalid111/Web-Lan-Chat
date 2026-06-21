from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    student_id: str
    name: str
    password: str

class UserLogin(BaseModel):
    student_id: str
    password: str

class UserResponse(BaseModel):
    id: int
    student_id: str
    name: str

    class Config:
        from_attributes = True
