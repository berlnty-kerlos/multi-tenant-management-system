from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.infrastructure.db.models import ProjectORM

class ProjectRepositoryImpl:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, *, tenant_id: UUID, name: str, description: Optional[ str ]) -> ProjectORM:
        orm = ProjectORM(tenant_id=tenant_id, name=name, description=description)
        self.db.add(orm)
        await self.db.flush()
        await self.db.refresh(orm)
        await self.db.commit()
        return orm

    async def list_by_tenant(self, tenant_id: UUID) -> List[ProjectORM]:
        res = await self.db.execute(select(ProjectORM).where(ProjectORM.tenant_id == tenant_id))
        return list(res.scalars().all())

    async def get_by_id_and_tenant(self, project_id: UUID, tenant_id: UUID) -> Optional[ProjectORM]:
        res = await self.db.execute(
            select(ProjectORM).where(ProjectORM.id == project_id, ProjectORM.tenant_id == tenant_id)
        )
        return res.scalars().first()

    async def get_by_name_and_tenant(self, project_name: str , tenant_id: UUID) -> Optional[ProjectORM]:
        res = await self.db.execute(
            select(ProjectORM).where(ProjectORM.name == project_name, ProjectORM.tenant_id == tenant_id)
        )
        return res.scalars().first()

    async def update(self, project_id: UUID, tenant_id: UUID, *, name: Optional[str], description: Optional[str ]) -> Optional[ProjectORM]:
        orm = await self.get_by_id_and_tenant(project_id, tenant_id)
        if not orm:
            return None
        if name is not None:
            orm.name = name
        if description is not None:
            orm.description = description
        await self.db.flush()
        await self.db.refresh(orm)
        await self.db.commit()
        return orm

    async def delete(self, project_id: UUID, tenant_id: UUID) -> bool:
        orm = await self.get_by_id_and_tenant(project_id, tenant_id)
        if (not orm):
            return False
        await self.db.delete(orm)
        await self.db.commit()
        return True
