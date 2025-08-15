from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    tenant_name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    tenant_name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshSchema(BaseModel):
    refresh_token: str