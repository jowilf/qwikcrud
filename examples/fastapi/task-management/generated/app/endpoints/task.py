from typing import Optional

from app import crud
from app.deps import SessionDep
from app.schemas import (ProjectOut, TaskCreate, TaskOut, TaskPatch,
                         TaskUpdate, UserOut)
from fastapi import APIRouter, UploadFile

router = APIRouter(tags=["tasks"])


@router.get("/")
async def read_all(db: SessionDep, skip: int = 0, limit: int = 100) -> list[TaskOut]:
    return await crud.task.get_all(db, skip=skip, limit=limit)


@router.get("/{id}")
async def read_one(db: SessionDep, id: int) -> TaskOut:
    task = await crud.task.getOr404(db, id)
    return task


@router.post("/", status_code=201)
async def create(*, db: SessionDep, task_in: TaskCreate) -> TaskOut:
    return await crud.task.create(db, obj_in=task_in)


@router.put("/{id}")
async def update(*, db: SessionDep, id: int, task_in: TaskUpdate) -> TaskOut:
    task = await crud.task.getOr404(db, id)
    return await crud.task.update(db, db_obj=task, obj_in=task_in)


@router.patch("/{id}")
async def patch(*, db: SessionDep, id: int, task_in: TaskPatch) -> TaskOut:
    task = await crud.task.getOr404(db, id)
    return await crud.task.update(db, db_obj=task, obj_in=task_in)


@router.delete("/{id}", status_code=204)
async def delete(*, db: SessionDep, id: int) -> None:
    task = await crud.task.getOr404(db, id)
    return await crud.task.delete(db, db_obj=task)


# Handle files


@router.put("/{id}/instructions")
async def set_instructions(*, db: SessionDep, id: int, file: UploadFile) -> TaskOut:
    task = await crud.task.getOr404(db, id)
    task.instructions = file
    return await crud.task.save(db, db_obj=task)


@router.delete("/{id}/instructions", status_code=204)
async def remove_instructions(*, db: SessionDep, id: int) -> None:
    task = await crud.task.getOr404(db, id)
    task.instructions = None
    await crud.task.save(db, db_obj=task)


# Handle relationships


@router.get("/{id}/project")
async def get_associated_project(db: SessionDep, id: int) -> Optional[ProjectOut]:
    task = await crud.task.getOr404(db, id)
    return task.project


@router.put("/{id}/project/{project_id}")
async def set_project_by_id(
    db: SessionDep, id: int, project_id: int
) -> Optional[ProjectOut]:
    task = await crud.task.getOr404(db, id)
    task.project = await crud.project.getOr404(db, project_id)
    task = await crud.task.save(db, task)
    return task.project


@router.get("/{id}/assignee")
async def get_associated_assignee(db: SessionDep, id: int) -> Optional[UserOut]:
    task = await crud.task.getOr404(db, id)
    return task.assignee


@router.put("/{id}/assignee/{assignee_id}")
async def set_assignee_by_id(
    db: SessionDep, id: int, assignee_id: int
) -> Optional[UserOut]:
    task = await crud.task.getOr404(db, id)
    task.assignee = await crud.user.getOr404(db, assignee_id)
    task = await crud.task.save(db, task)
    return task.assignee
