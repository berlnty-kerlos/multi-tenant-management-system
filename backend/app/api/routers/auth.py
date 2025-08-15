
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_db
from app.api.schemas.auth import RegisterSchema, LoginSchema, TokenResponse,TokenRefreshSchema
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.tenant_repository_impl import TenantRepositoryImpl
from app.infrastructure.auth import jwt as jwt_utils, refresh as refresh_utils
from app.api.dependancies import get_current_user, require_role
from app.core.exceptions import ServiceError

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterSchema, db: AsyncSession = Depends(get_db)):
    try:
        user_repo = UserRepositoryImpl(db)
        tenant_repo = TenantRepositoryImpl(db)
        service = AuthService(user_repo, tenant_repo)
   
        await service.register(
        tenant_name=payload.tenant_name,
        email=payload.email,
        password=payload.password
        )
        result = await service.login(
        tenant_name=payload.tenant_name,
        email=payload.email,
        password=payload.password
        )
        access_token = jwt_utils.create_access_token(
        subject=result["user_id"],
        tenant_id=result["tenant_id"]
        )
        refresh_token,_ = await refresh_utils.create_refresh_token(
            db, 
            user_id=result["user_id"],
            tenant_id=result["tenant_id"]
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e
 
   

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    try:
        user_repo = UserRepositoryImpl(db)
        tenant_repo = TenantRepositoryImpl(db)
        service = AuthService(user_repo, tenant_repo)


        result = await service.login(
        tenant_name=payload.tenant_name,
        email=payload.email,
        password=payload.password
        )


        access_token = jwt_utils.create_access_token(
        subject=result["user_id"],
        tenant_id=result["tenant_id"]
    )

        refresh_token,_ = await refresh_utils.create_refresh_token(
            db, 
            user_id=result["user_id"],
            tenant_id=result["tenant_id"]
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: TokenRefreshSchema, db: AsyncSession = Depends(get_db)):
    try:
        token_row = await refresh_utils.validate_refresh_token(db, payload.refresh_token)
        if not token_row:
            raise HTTPException(status_code=401, detail="invalid refresh token")
        user_id = str(token_row.user_id)
        tenant_id = str(token_row.tenant_id)

        # Issue new tokens
        access_token = jwt_utils.create_access_token( subject=user_id, tenant_id=tenant_id)
        new_refresh_token_raw, _ = await refresh_utils.create_refresh_token(db, user_id, tenant_id)

        # revoke old token 
        await refresh_utils.revoke_refresh_token(db, token_row.id)

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token_raw)
    except ServiceError  as e:
        raise  HTTPException(status_code=e.status_code, detail= e.detail)
    except Exception as e:
        raise e

