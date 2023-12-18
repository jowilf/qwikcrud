from typing import List, Optional

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
    task = await crud.task.get_or_404(db, id)
    return task


@router.post("/", status_code=201)
async def create(*, db: SessionDep, task_in: TaskCreate) -> TaskOut:
    return await crud.task.create(db, obj_in=task_in)


@router.put("/{id}")
async def update(*, db: SessionDep, id: int, task_in: TaskUpdate) -> TaskOut:
    task = await crud.task.get_or_404(db, id)
    return await crud.task.update(db, db_obj=task, obj_in=task_in)


@router.patch("/{id}")
async def patch(*, db: SessionDep, id: int, task_in: TaskPatch) -> TaskOut:
    task = await crud.task.get_or_404(db, id)
    return await crud.task.update(db, db_obj=task, obj_in=task_in)


@router.delete("/{id}", status_code=204)
async def delete(*, db: SessionDep, id: int) -> None:
    task = await crud.task.get_or_404(db, id)
    return await crud.task.delete(db, db_obj=task)


# Handle files


@router.put("/{id}/instruction_file")
async def set_instruction_file(*, db: SessionDep, id: int, file: UploadFile) -> TaskOut:
    task = await crud.task.get_or_404(db, id)
    task.instruction_file = file
    return await crud.task.save(db, db_obj=task)


@router.delete("/{id}/instruction_file", status_code=204)
async def remove_instruction_file(*, db: SessionDep, id: int) -> None:
    task = await crud.task.get_or_404(db, id)
    task.instruction_file = None
    await crud.task.save(db, db_obj=task)


# Handle relationships


@router.get("/{id}/project")
async def get_associated_project(db: SessionDep, id: int) -> Optional[ProjectOut]:
    task = await crud.task.get_or_404(db, id)
    return task.project


@router.put("/{id}/project/{project_id}")
async def set_project_by_id(
    db: SessionDep, id: int, project_id: int
) -> Optional[ProjectOut]:
    task = await crud.task.get_or_404(db, id)
    task.project = await crud.project.get_or_404(db, project_id)
    task = await crud.task.save(db, task)
    return task.project


@router.get("/{id}/assigned_users")
async def get_associated_assigned_users(db: SessionDep, id: int) -> List[UserOut]:
    task = await crud.task.get_or_404(db, id)
    return task.assigned_users


@router.put("/{id}/assigned_users")
async def add_assigned_users_by_ids(
    db: SessionDep, id: int, ids: List[int]
) -> List[UserOut]:
    task = await crud.task.get_or_404(db, id)
    for _id in ids:
        task.assigned_users.append(await crud.user.get_or_404(db, _id))
    task = await crud.task.save(db, task)
    return task.assigned_users
