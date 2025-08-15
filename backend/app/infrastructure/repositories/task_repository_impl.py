from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.db.models import TaskORM, TaskStatusEnum

class TaskRepositoryImpl:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, *, tenant_id: UUID, project_id: UUID, title: str, description: Optional[str ], assignee_id: Optional[ UUID ]) -> TaskORM:
        orm = TaskORM(
            tenant_id=tenant_id,
            project_id=project_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
        )
        self.db.add(orm)
        await self.db.flush()
        await self.db.refresh(orm)
        await self.db.commit()
        return orm

    async def list_by_project(self, project_id: UUID, tenant_id: UUID) -> List[TaskORM]:
        res = await self.db.execute(
            select(TaskORM).where(TaskORM.project_id == project_id, TaskORM.tenant_id == tenant_id)
        )
        return list(res.scalars().all())

    async def get_by_id_and_tenant(self, task_id: UUID, tenant_id: UUID) -> Optional[TaskORM]:
        res = await self.db.execute(
            select(TaskORM).where(TaskORM.id == task_id, TaskORM.tenant_id == tenant_id)
        )
        return res.scalars().first()

    async def update(
        self,
        task_id: UUID,
        tenant_id: UUID,
        *,
        title: Optional[str ] = None,
        description: Optional[str ] = None,
        status: Optional[TaskStatusEnum ] = None,
        assignee_id: Optional[UUID ] = None,
    ) -> Optional[TaskORM]:
        orm = await self.get_by_id_and_tenant(task_id, tenant_id)
        if not orm:
            return None
        if title is not None:
            orm.title = title
        if description is not None:
            orm.description = description
        if status is not None:
            orm.status = status
        if assignee_id is not None or assignee_id is None:
            orm.assignee_id = assignee_id
        await self.db.flush()
        await self.db.refresh(orm)
        await self.db.commit()
        return orm

    async def delete(self, task_id: UUID, tenant_id: UUID) -> bool:
        orm = await self.get_by_id_and_tenant(task_id, tenant_id)
        if not orm:
            return False
        await self.db.delete(orm)
        await self.db.commit()
        return True
