from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar, Union

from app.models import Project, Task, User
from app.schemas import (ProjectCreate, ProjectUpdate, TaskCreate, TaskUpdate,
                         UserCreate, UserUpdate)
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.get(self.model, id)

    async def getOr404(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = await self.get(db, id)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} with id: {id} not found"
            )
        return obj

    async def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    async def save(self, db: Session, db_obj: ModelType) -> ModelType:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())  # type: ignore
        return await self.save(db, db_obj)

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        return await self.save(db, db_obj)

    async def delete(self, db: Session, *, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


user = CRUDUser(User)
project = CRUDProject(Project)
task = CRUDTask(Task)
