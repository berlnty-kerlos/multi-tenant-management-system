import os
from app.api.dependancies import require_role
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.db.base import Base
from app.infrastructure.db.session  import get_db
from app.main import app
from httpx import AsyncClient

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/management_system_test_db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Override get_db
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Create tables before tests
@pytest.fixture(scope="module", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Async test client
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
