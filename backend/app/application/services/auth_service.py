from uuid import uuid4
from passlib.hash import bcrypt

from app.core.exceptions import ServiceError
from app.core.http_status import HTTPStatus as status
from app.domain.models import User, Tenant
from app.domain.repositories import UserRepository, TenantRepository

class AuthService:
    def __init__(self, user_repo: UserRepository, tenant_repo: TenantRepository):
        self.user_repo = user_repo
        self.tenant_repo = tenant_repo

    async def register(self, tenant_name: str, email: str, password: str):
        tenant = await self.tenant_repo.get_by_name(tenant_name)
        if not tenant:
            raise ServiceError(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")
        # tenant = Tenant(id=uuid4(), name=tenant_name)
        # await self.tenant_repo.create(tenant)
        hashed_pw = bcrypt.hash(password)
        user = User(
            id=uuid4(),
            tenant_id=tenant.id,
            email=email,
            hashed_password=hashed_pw
        )
        await self.user_repo.create(user)
        return {"tenant_id": str(tenant.id), "user_id": str(user.id)}

    async def login(self, tenant_name: str, email: str, password: str):
        tenant = await self.tenant_repo.get_by_name(tenant_name)
        if not tenant:
            raise ServiceError(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")

        user = await self.user_repo.get_by_email(tenant.id, email)
        if not user or not bcrypt.verify(password, user.hashed_password):
            raise ServiceError(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

        return {
            "user_id": str(user.id),
            "tenant_id": str(tenant.id),
            "role": user.role
        }
