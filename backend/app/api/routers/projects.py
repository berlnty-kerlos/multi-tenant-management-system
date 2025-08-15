from typing import List
from app.core.exceptions import ServiceError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.infrastructure.db.session import get_db
from app.api.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.application.services.project_service import ProjectService
from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.api.dependancies import get_current_user 

router = APIRouter()

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = ProjectService(ProjectRepositoryImpl(db))
        project = await service.create(current_user.tenant_id, data)
        return project
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e
 

@router.get("", response_model=List[ProjectOut])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = ProjectService(ProjectRepositoryImpl(db))
        return await service.list(current_user.tenant_id)
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = ProjectService(ProjectRepositoryImpl(db))
        project = await service.get(current_user.tenant_id, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = ProjectService(ProjectRepositoryImpl(db))
        project = await service.update(current_user.tenant_id, project_id, data)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        service = ProjectService(ProjectRepositoryImpl(db))
        ok = await service.delete(current_user.tenant_id, project_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Project not found")
        return None
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e