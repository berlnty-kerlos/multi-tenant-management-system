import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.enums import UserRole, TaskStatusEnum
import uuid
from app.infrastructure.db.base import Base


class TenantORM(Base):
    __tablename__ = "tenants"
    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String, nullable=False, unique=True)
    domain = sa.Column(sa.String, nullable=True, unique=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())

class UserORM(Base):
    __tablename__ = "users"
    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    email = sa.Column(sa.String, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.String, nullable=False, default=UserRole.USER.value)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())

    tenant = relationship("TenantORM")

class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"
    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = sa.Column(sa.String, nullable=False)
    expires_at = sa.Column(sa.DateTime, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())

    user = relationship("UserORM")
    tenant = relationship("TenantORM")


class ProjectORM(Base):
    __tablename__ = "projects"
    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    tenant_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tenant = relationship("TenantORM")
    tasks = relationship("TaskORM", back_populates="project", cascade="all, delete-orphan")

class TaskORM(Base):
    __tablename__ = "tasks"
    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    status = sa.Column(sa.Enum(TaskStatusEnum, name="task_status_enum"), nullable=False, server_default="todo")
    assignee_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    project_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id = sa.Column(PG_UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    project = relationship("ProjectORM", back_populates="tasks")
    tenant = relationship("TenantORM")
    assignee = relationship("UserORM")