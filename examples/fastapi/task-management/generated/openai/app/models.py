import datetime
from typing import List, Optional, Union

from app.enums import Status
from fastapi import UploadFile
from pydantic import EmailStr
from sqlalchemy import JSON, Column, Enum, ForeignKey, MetaData, String, Table
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


task__users = Table(
    "task__users",
    Base.metadata,
    Column("task_id", ForeignKey("task.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[EmailStr] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    avatar: Mapped[Union[File, UploadFile, None]] = mapped_column(
        ImageField(
            thumbnail_size=(150, 150), validators=[SizeValidator(max_size="20M")]
        )
    )
    bio: Mapped[str]

    projects: Mapped[List["Project"]] = relationship(back_populates="user")

    tasks: Mapped[List["Task"]] = relationship(
        secondary=task__users, back_populates="assigned_users"
    )


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[datetime.date]
    due_date: Mapped[datetime.date]

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="projects")

    tasks: Mapped[List["Task"]] = relationship(back_populates="project")


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[datetime.date]
    due_date: Mapped[datetime.date]
    status: Mapped[str] = mapped_column(Enum(Status))
    instruction_file: Mapped[Union[File, UploadFile, None]] = mapped_column(
        FileField(
            validators=[
                SizeValidator(max_size="20M"),
                ContentTypeValidator(
                    ["application/pdf", "application/msword", "text/plain"]
                ),
            ]
        )
    )

    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project.id"))
    project: Mapped["Project"] = relationship(back_populates="tasks")

    assigned_users: Mapped[List["User"]] = relationship(
        secondary=task__users, back_populates="tasks"
    )
