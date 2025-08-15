from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from app.domain.models import User
from app.domain.repositories import UserRepository
from app.infrastructure.db import models as orm_models

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, tenant_id: UUID, email: str) -> Optional[User]:
        q = select(orm_models.UserORM).where(
            orm_models.UserORM.tenant_id == tenant_id,
            orm_models.UserORM.email == email
        )
        res = await self.db.execute(q)
        row = res.scalars().first()
        if not row:
            return None
        return User(
            id=row.id,
            tenant_id=row.tenant_id,
            email=row.email,
            hashed_password=row.hashed_password,
            role=row.role,
            created_at=row.created_at
        )

    async def create(self, user: User) -> User:
        db_user = orm_models.UserORM(**user.__dict__)
        self.db.add(db_user)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(db_user) 
        return user
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        q = select(orm_models.UserORM).where(orm_models.UserORM.id == user_id)
        res = await self.db.execute(q)
        row = res.scalars().first()
        if not row:
            return None
        return User(
            id=row.id,
            tenant_id=row.tenant_id,
            email=row.email,
            hashed_password=row.hashed_password,
            role=row.role,
            created_at=row.created_at
    )