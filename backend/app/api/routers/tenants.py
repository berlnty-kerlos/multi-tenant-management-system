from app.core.exceptions import ServiceError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_db
from app.application.services.tenant_service import TenantService
from app.infrastructure.repositories.tenant_repository_impl import TenantRepositoryImpl
from app.api.schemas.tenant import TenantCreate  
from app.api.dependancies import  require_role
from app.core.enums import UserRole

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_in: TenantCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(UserRole.ADMIN))
):
    try:
        tenant_repo = TenantRepositoryImpl(db)
        service = TenantService(tenant_repo)
  
        tenant = await service.create_tenant(tenant_in)
        return tenant
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e