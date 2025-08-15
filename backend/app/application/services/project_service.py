from uuid import UUID
from typing import List

from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.api.schemas.project import ProjectCreate, ProjectUpdate
from app.infrastructure.db.models import ProjectORM
from app.core.exceptions import ServiceError
from app.core.http_status import HTTPStatus as status


class ProjectService:
    def __init__(self, project_repo: ProjectRepositoryImpl):
        self.project_repo = project_repo

    async def create(self, tenant_id: UUID, data: ProjectCreate) -> ProjectORM:
        existing = await self.project_repo.get_by_name_and_tenant(data.name, tenant_id)
        if existing:
            raise ServiceError(status.HTTP_409_CONFLICT, f"Project '{data.name}' already exists")

        return await self.project_repo.create(
            tenant_id=tenant_id,
            name=data.name,
            description=data.description,
        )

    async def list(self, tenant_id: UUID) -> List[ProjectORM]:
        return await self.project_repo.list_by_tenant(tenant_id)

    async def get(self, tenant_id: UUID, project_id: UUID) -> ProjectORM:
        project = await self.project_repo.get_by_id_and_tenant(project_id, tenant_id)
        if not project:
            raise ServiceError(status.HTTP_404_NOT_FOUND, "Project not found")
        return project

    async def update(self, tenant_id: UUID, project_id: UUID, data: ProjectUpdate) -> ProjectORM:
        project = await self.project_repo.get_by_id_and_tenant(project_id, tenant_id)
        if not project:
            raise ServiceError(status.HTTP_404_NOT_FOUND, "Project not found")

        updated = await self.project_repo.update(
            project_id=project_id,
            tenant_id=tenant_id,
            name=data.name,
            description=data.description,
        )
        if not updated:
            raise ServiceError(status.INTERNAL_SERVER_ERROR, "Failed to update project")
        return updated

    async def delete(self, tenant_id: UUID, project_id: UUID) -> bool:
        deleted = await self.project_repo.delete(project_id, tenant_id)
        if not deleted:
            raise ServiceError(status.HTTP_404_NOT_FOUND, "Project not found")
        return deleted
