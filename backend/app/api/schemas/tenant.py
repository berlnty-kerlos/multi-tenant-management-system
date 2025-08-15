from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str
    domain: str

    class Config:
        orm_mode = True