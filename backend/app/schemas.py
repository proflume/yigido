from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


class TaskRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True
