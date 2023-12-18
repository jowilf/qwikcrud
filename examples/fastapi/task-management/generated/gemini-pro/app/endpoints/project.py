from typing import List

from app import crud
from app.deps import SessionDep
from app.schemas import (ProjectCreate, ProjectOut, ProjectPatch,
                         ProjectUpdate, TaskOut, UserOut)
from fastapi import APIRouter

router = APIRouter(tags=["projects"])


@router.get("/")
async def read_all(db: SessionDep, skip: int = 0, limit: int = 100) -> list[ProjectOut]:
    return await crud.project.get_all(db, skip=skip, limit=limit)


@router.get("/{id}")
async def read_one(db: SessionDep, id: int) -> ProjectOut:
    project = await crud.project.get_or_404(db, id)
    return project


@router.post("/", status_code=201)
async def create(*, db: SessionDep, project_in: ProjectCreate) -> ProjectOut:
    return await crud.project.create(db, obj_in=project_in)


@router.put("/{id}")
async def update(*, db: SessionDep, id: int, project_in: ProjectUpdate) -> ProjectOut:
    project = await crud.project.get_or_404(db, id)
    return await crud.project.update(db, db_obj=project, obj_in=project_in)


@router.patch("/{id}")
async def patch(*, db: SessionDep, id: int, project_in: ProjectPatch) -> ProjectOut:
    project = await crud.project.get_or_404(db, id)
    return await crud.project.update(db, db_obj=project, obj_in=project_in)


@router.delete("/{id}", status_code=204)
async def delete(*, db: SessionDep, id: int) -> None:
    project = await crud.project.get_or_404(db, id)
    return await crud.project.delete(db, db_obj=project)


# Handle relationships


@router.get("/{id}/users")
async def get_associated_users(db: SessionDep, id: int) -> List[UserOut]:
    project = await crud.project.get_or_404(db, id)
    return project.users


@router.put("/{id}/users")
async def add_users_by_ids(db: SessionDep, id: int, ids: List[int]) -> List[UserOut]:
    project = await crud.project.get_or_404(db, id)
    for _id in ids:
        project.users.append(await crud.user.get_or_404(db, _id))
    project = await crud.project.save(db, project)
    return project.users


@router.get("/{id}/tasks")
async def get_associated_tasks(db: SessionDep, id: int) -> List[TaskOut]:
    project = await crud.project.get_or_404(db, id)
    return project.tasks


@router.put("/{id}/tasks")
async def add_tasks_by_ids(db: SessionDep, id: int, ids: List[int]) -> List[TaskOut]:
    project = await crud.project.get_or_404(db, id)
    for _id in ids:
        project.tasks.append(await crud.task.get_or_404(db, _id))
    project = await crud.project.save(db, project)
    return project.tasks
