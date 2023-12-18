import datetime
from typing import Optional

from app.enums import Status
from pydantic import BaseModel, EmailStr, Field


class Thumbnail(BaseModel):
    path: str


class FileInfo(BaseModel):
    filename: str
    content_type: str
    path: str
    thumbnail: Optional[Thumbnail] = None


# -------------- User ------------------


class UserCreate(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    bio: str


class UserUpdate(UserCreate):
    pass


class UserPatch(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None)


class UserOut(BaseModel):
    id: int
    username: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    avatar: Optional[FileInfo]
    bio: str


# -------------- Project ------------------


class ProjectCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str
    start_date: datetime.date
    due_date: datetime.date


class ProjectUpdate(ProjectCreate):
    pass


class ProjectPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    start_date: Optional[datetime.date] = Field(None)
    due_date: Optional[datetime.date] = Field(None)


class ProjectOut(BaseModel):
    id: int
    name: str = Field(max_length=100)
    description: str
    start_date: datetime.date
    due_date: datetime.date


# -------------- Task ------------------


class TaskCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str
    start_date: datetime.date
    due_date: datetime.date
    status: Status


class TaskUpdate(TaskCreate):
    pass


class TaskPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    start_date: Optional[datetime.date] = Field(None)
    due_date: Optional[datetime.date] = Field(None)
    status: Optional[Status] = Field(None)


class TaskOut(BaseModel):
    id: int
    name: str = Field(max_length=100)
    description: str
    start_date: datetime.date
    due_date: datetime.date
    status: Status
    instruction_file: Optional[FileInfo] = Field(
        mime_types=["application/pdf", "application/msword", "text/plain"]
    )
