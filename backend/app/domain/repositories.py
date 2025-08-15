from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.models import User, Tenant, RefreshToken

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, tenant_id: UUID, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

class TenantRepository(ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Tenant]:
        pass

    @abstractmethod
    async def create(self, tenant: Tenant) -> Tenant:
        pass

class RefreshTokenRepository(ABC):
    @abstractmethod
    async def create(self, token: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    async def get_by_token(self, token_hash: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    async def delete(self, token_id: UUID) -> None:
        pass
