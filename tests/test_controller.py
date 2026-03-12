import pytest_asyncio
import pytest
from http import HTTPStatus
from httpx import AsyncClient, ASGITransport
from src.correios_cep.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://lobotest"
    ) as client:
        yield client

