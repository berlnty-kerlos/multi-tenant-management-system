from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.enums import UserRole

@dataclass
class Tenant:
    id: UUID
    name: str
    domain: Optional[str ] = None
    created_at: Optional[datetime ] = None

@dataclass
class User:
    id: UUID
    tenant_id: UUID
    email: str
    hashed_password: str
    role: UserRole = UserRole.USER.value
    created_at:Optional[ datetime ] = None

@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    tenant_id: UUID
    token_hash: str
    expires_at: datetime
    created_at: Optional[datetime ] = None