from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.infrastructure.db import models as orm_models
from app.domain.models import Tenant

class TenantRepositoryImpl:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Optional[Tenant ]:
        stmt = select(orm_models.TenantORM).where(orm_models.TenantORM.name == name)
        res = await self.db.execute(stmt)
        row = res.scalars().first()
        if row:
            return Tenant(
                id=row.id,
                name=row.name,
                domain=row.domain,
                created_at=row.created_at
            )
        return None

    async def create(self, tenant: Tenant) -> Tenant:
        tenant_orm = orm_models.TenantORM(name=tenant.name, domain= tenant.domain)
        self.db.add(tenant_orm)
        await self.db.flush() 
        await self.db.commit() 
        await self.db.refresh(tenant_orm) 

        return Tenant(
            id=tenant_orm.id,
            name=tenant_orm.name,
            domain=tenant_orm.domain,
            created_at=tenant_orm.created_at
        )
    async def delete(self, tenant_id: UUID) -> bool:
      
        stmt = select(orm_models.TenantORM).where(orm_models.TenantORM.id == tenant_id)
        res = await self.db.execute(stmt)
        tenant_orm = res.scalars().first()
        if not tenant_orm:
            return False

        await self.db.delete(tenant_orm)
        await self.db.commit()
        return True