from typing import List, Optional

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


@router.get("/{id}/user")
async def get_associated_user(db: SessionDep, id: int) -> Optional[UserOut]:
    project = await crud.project.get_or_404(db, id)
    return project.user


@router.put("/{id}/user/{user_id}")
async def set_user_by_id(db: SessionDep, id: int, user_id: int) -> Optional[UserOut]:
    project = await crud.project.get_or_404(db, id)
    project.user = await crud.user.get_or_404(db, user_id)
    project = await crud.project.save(db, project)
    return project.user


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
