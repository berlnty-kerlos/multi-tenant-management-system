import hashlib
import uuid
from datetime import datetime, timedelta
from app.infrastructure.db.models import RefreshTokenORM
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.settings import settings  
import os


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def create_refresh_token(db: AsyncSession, user_id, tenant_id):
    raw = str(uuid.uuid4())
    token_hash = _hash_token(raw)
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    rt = RefreshTokenORM(user_id=user_id, tenant_id=tenant_id, token_hash=token_hash, expires_at=expires_at)
    db.add(rt)
    await db.commit()
    await db.refresh(rt)
    return raw, rt

async def rotate_refresh_token(db: AsyncSession, token_id, user_id, tenant_id):
    # delete old + create new
    await db.execute(delete(RefreshTokenORM).where(RefreshTokenORM.id == token_id))
    await db.commit()
    return await create_refresh_token(db, user_id, tenant_id)

async def validate_refresh_token(db: AsyncSession, raw_token: str):
    h = _hash_token(raw_token)
    q = select(RefreshTokenORM).where(RefreshTokenORM.token_hash == h)
    res = await db.execute(q)
    row = res.scalars().first()
    if not row:
        return None
    if row.expires_at < datetime.utcnow():
        # expired: delete
        await db.delete(row)
        await db.commit()
        return None
    return row

async def revoke_refresh_token(db: AsyncSession, token_id):
    await db.execute(delete(RefreshTokenORM).where(RefreshTokenORM.id == token_id))
    await db.commit()

