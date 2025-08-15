import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependancies import require_role
from app.infrastructure.db.session import get_db

from app.infrastructure.repositories.tenant_repository_impl import TenantRepositoryImpl

@pytest.fixture
def client():
    yield TestClient(app)
