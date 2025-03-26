import pytest
from starlette.testclient import TestClient

from app.interface.api import create_app


@pytest.fixture
async def client_test_default():  # noqa: RUF029
    return TestClient(create_app())
