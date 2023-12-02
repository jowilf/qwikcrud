from typing import List

from app import crud
from app.deps import SessionDep
from app.schemas import (ProjectOut, TaskOut, UserCreate, UserOut, UserPatch,
                         UserUpdate)
from fastapi import APIRouter, UploadFile

router = APIRouter(tags=["users"])


@router.get("/")
async def read_all(db: SessionDep, skip: int = 0, limit: int = 100) -> list[UserOut]:
    return await crud.user.get_all(db, skip=skip, limit=limit)


@router.get("/{id}")
async def read_one(db: SessionDep, id: int) -> UserOut:
    user = await crud.user.get_or_404(db, id)
    return user


@router.post("/", status_code=201)
async def create(*, db: SessionDep, user_in: UserCreate) -> UserOut:
    return await crud.user.create(db, obj_in=user_in)


@router.put("/{id}")
async def update(*, db: SessionDep, id: int, user_in: UserUpdate) -> UserOut:
    user = await crud.user.get_or_404(db, id)
    return await crud.user.update(db, db_obj=user, obj_in=user_in)


@router.patch("/{id}")
async def patch(*, db: SessionDep, id: int, user_in: UserPatch) -> UserOut:
    user = await crud.user.get_or_404(db, id)
    return await crud.user.update(db, db_obj=user, obj_in=user_in)


@router.delete("/{id}", status_code=204)
async def delete(*, db: SessionDep, id: int) -> None:
    user = await crud.user.get_or_404(db, id)
    return await crud.user.delete(db, db_obj=user)


# Handle files


@router.put("/{id}/avatar")
async def set_avatar(*, db: SessionDep, id: int, file: UploadFile) -> UserOut:
    user = await crud.user.get_or_404(db, id)
    user.avatar = file
    return await crud.user.save(db, db_obj=user)


@router.delete("/{id}/avatar", status_code=204)
async def remove_avatar(*, db: SessionDep, id: int) -> None:
    user = await crud.user.get_or_404(db, id)
    user.avatar = None
    await crud.user.save(db, db_obj=user)


# Handle relationships


@router.get("/{id}/projects")
async def get_associated_projects(db: SessionDep, id: int) -> List[ProjectOut]:
    user = await crud.user.get_or_404(db, id)
    return user.projects


@router.put("/{id}/projects")
async def add_projects_by_ids(
    db: SessionDep, id: int, ids: List[int]
) -> List[ProjectOut]:
    user = await crud.user.get_or_404(db, id)
    for _id in ids:
        user.projects.append(await crud.project.get_or_404(db, _id))
    user = await crud.user.save(db, user)
    return user.projects


@router.get("/{id}/tasks")
async def get_associated_tasks(db: SessionDep, id: int) -> List[TaskOut]:
    user = await crud.user.get_or_404(db, id)
    return user.tasks


@router.put("/{id}/tasks")
async def add_tasks_by_ids(db: SessionDep, id: int, ids: List[int]) -> List[TaskOut]:
    user = await crud.user.get_or_404(db, id)
    for _id in ids:
        user.tasks.append(await crud.task.get_or_404(db, _id))
    user = await crud.user.save(db, user)
    return user.tasks
