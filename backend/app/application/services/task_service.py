from uuid import UUID
from typing import List, Optional

from app.core.exceptions import ServiceError
from app.core.http_status import HTTPStatus as status
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.api.schemas.task import TaskCreate, TaskUpdate
from app.infrastructure.db.models import TaskORM, TaskStatusEnum

class TaskService:
    def __init__(self, task_repo: TaskRepositoryImpl, project_repo: ProjectRepositoryImpl, user_repo: UserRepositoryImpl):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.user_repo = user_repo

    async def _ensure_project_in_tenant(self, tenant_id: UUID, project_id: UUID):
        project = await self.project_repo.get_by_id_and_tenant(project_id, tenant_id)
        if not project:
            raise ServiceError(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def _ensure_assignee_in_tenant(self, tenant_id: UUID, assignee_id: Optional[UUID ]):
        if assignee_id is None:
            return
        assignee = await self.user_repo.get_by_id(assignee_id)
        if not assignee or assignee.tenant_id != tenant_id:
            raise ServiceError(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee must belong to the same tenant")

    async def create(self, tenant_id: UUID, project_id: UUID, data: TaskCreate) -> TaskORM:
        await self._ensure_project_in_tenant(tenant_id, project_id)
        if data.assignee_id:
            await self._ensure_assignee_in_tenant(tenant_id, data.assignee_id)
        return await self.task_repo.create(
            tenant_id=tenant_id,
            project_id=project_id,
            title=data.title,
            description=data.description,
            assignee_id=data.assignee_id,     
        )

    async def list_by_project(self, tenant_id: UUID, project_id: UUID) -> List[TaskORM]:
        await self._ensure_project_in_tenant(tenant_id, project_id)
        return await self.task_repo.list_by_project(project_id, tenant_id)

    async def update(self, tenant_id: UUID, task_id: UUID, data: TaskUpdate) -> TaskORM:
        task = await self.task_repo.get_by_id_and_tenant(task_id, tenant_id)
        if not task:
            raise ServiceError(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        if data.assignee_id:
            await self._ensure_assignee_in_tenant(tenant_id, data.assignee_id)

        updated = await self.task_repo.update(
            task_id=task_id,
            tenant_id=tenant_id,
            title=data.title,
            description=data.description,
            status=TaskStatusEnum(data.status) if data.status is not None else None,
            assignee_id=data.assignee_id if "assignee_id" in data.model_fields_set else None,
        )
        if not updated:
            raise RuntimeError("Unexpected: task update returned None")
        return updated

    async def delete(self, tenant_id: UUID, task_id: UUID) -> bool:
        return await self.task_repo.delete(task_id, tenant_id)
