from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class ImageProcessingRequest(BaseModel):
    image_url: str
    operations: List[str]

class ImageProcessingResponse(BaseModel):
    job_id: int
    status: str
    message: str

class TaskRequest(BaseModel):
    task_name: str
    duration: float = 1.0