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

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class AnnouncementCreate(BaseModel):
    title: str
    content: str

class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

    class Config:
        from_attributes = True
