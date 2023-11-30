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
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    bio: str


class UserUpdate(UserCreate):
    pass


class UserPatch(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    firstname: Optional[str] = Field(None, max_length=50)
    lastname: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None)


class UserOut(BaseModel):
    id: int
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    avatar: Optional[FileInfo]
    bio: str


# -------------- Project ------------------


class ProjectCreate(BaseModel):
    title: str = Field(max_length=100)
    description: str


class ProjectUpdate(ProjectCreate):
    pass


class ProjectPatch(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)


class ProjectOut(BaseModel):
    id: int
    title: str = Field(max_length=100)
    description: str


# -------------- Task ------------------


class TaskCreate(BaseModel):
    name: str = Field(max_length=500)
    startdate: datetime.date
    duedate: datetime.date
    status: Status


class TaskUpdate(TaskCreate):
    pass


class TaskPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=500)
    startdate: Optional[datetime.date] = Field(None)
    duedate: Optional[datetime.date] = Field(None)
    status: Optional[Status] = Field(None)


class TaskOut(BaseModel):
    id: int
    name: str = Field(max_length=500)
    startdate: datetime.date
    duedate: datetime.date
    status: Status
    instructions: Optional[FileInfo] = Field(
        mime_types=["application/pdf", "text/plain"]
    )