from typing import List
from app.core.exceptions import ServiceError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.infrastructure.db.session import get_db
from app.api.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.application.services.task_service import TaskService
from app.application.services.project_service import ProjectService
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.api.dependancies import get_current_user

router = APIRouter()

def _task_service(db: AsyncSession) -> TaskService:
    return TaskService(
        task_repo=TaskRepositoryImpl(db),
        project_repo=ProjectRepositoryImpl(db),
        user_repo=UserRepositoryImpl(db),
    )

@router.post("/projects/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: UUID,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = _task_service(db)
        task = await service.create(current_user.tenant_id, project_id, data)
        return task
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.get("/projects/{project_id}/tasks", response_model=List[TaskOut])
async def list_tasks(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = _task_service(db)
        return await service.list_by_project(current_user.tenant_id, project_id)
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = _task_service(db)
        return await service.update(current_user.tenant_id, task_id, data)
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = _task_service(db)
        ok = await service.delete(current_user.tenant_id, task_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Task not found")
        return None

    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e