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


@pytest.mark.asyncio
async def test_get_by_zip_code(client):
    zipcode = "36803000"
    response = await client.get(f"/zip/{zipcode}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "state": "MG",
        "city": "Carangola",
        "Neighborhood": "Alvorada",
        "zipcode": "36803000",
        "street": ""
    }


@pytest.mark.asyncio
async def test_get_by_zip_code_empty_validation(client):
    response = await client.get("/zip/")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": "CEP não pode ser vazio"
    }


@pytest.mark.asyncio
async def test_get_by_zip_code_404(client):
    zipcode = "00000000"
    response = await client.get(f"/zip/{zipcode}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": f"CEP {zipcode} não encontrado"
    }


