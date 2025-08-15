import pytest
from tests.utils import client
from app.api.schemas.tenant import TenantCreate
import uuid
import os
from app.core.settings import settings
from app.main import app

