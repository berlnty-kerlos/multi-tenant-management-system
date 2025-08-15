from app.domain.models import Tenant
from app.infrastructure.repositories.tenant_repository_impl import TenantRepositoryImpl

class TenantService:
    def __init__(self, tenant_repo: TenantRepositoryImpl):
        self.tenant_repo = tenant_repo

    async def create_tenant(self, tenant_data: Tenant) -> Tenant:
        existing = await self.tenant_repo.get_by_name(tenant_data.name)
        if existing:
            raise ValueError("Tenant already exists")

        new_tenant = await self.tenant_repo.create(tenant_data)
        return new_tenant