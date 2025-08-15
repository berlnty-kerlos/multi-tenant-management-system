from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime
from app.core.enums import TaskStatusEnum



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatusEnum] = None
    assignee_id: Optional[UUID] = None

class TaskOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatusEnum
    assignee_id: Optional[UUID]
    project_id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
