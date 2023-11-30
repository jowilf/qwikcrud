import datetime
from typing import List, Optional, Union

from app.enums import Status
from fastapi import UploadFile
from pydantic import EmailStr
from sqlalchemy import JSON, Enum, ForeignKey, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_file import File, FileField, ImageField
from sqlalchemy_file.validators import ContentTypeValidator, SizeValidator


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        onupdate=datetime.datetime.utcnow
    )


class Base(DeclarativeBase, TimestampMixin):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    type_annotation_map = {EmailStr: String, dict: JSON}


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[EmailStr] = mapped_column(unique=True)
    password: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    avatar: Mapped[Union[File, UploadFile, None]] = mapped_column(
        ImageField(
            thumbnail_size=(150, 150), validators=[SizeValidator(max_size="20M")]
        )
    )
    bio: Mapped[str]

    projects: Mapped[List["Project"]] = relationship(back_populates="user")

    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task.id"))
    task: Mapped["Task"] = relationship(back_populates="assignee")


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="projects")

    tasks: Mapped[List["Task"]] = relationship(back_populates="project")


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    startdate: Mapped[datetime.date]
    duedate: Mapped[datetime.date]
    status: Mapped[str] = mapped_column(Enum(Status))
    instructions: Mapped[Union[File, UploadFile, None]] = mapped_column(
        FileField(
            validators=[
                SizeValidator(max_size="20M"),
                ContentTypeValidator(["application/pdf", "text/plain"]),
            ]
        )
    )

    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project.id"))
    project: Mapped["Project"] = relationship(back_populates="tasks")

    assignee: Mapped["User"] = relationship(back_populates="task")
