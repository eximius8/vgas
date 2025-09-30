import pytest
from httpx import AsyncClient, ASGITransport

from backend.main import app


@pytest.mark.asyncio
async def test_create_job():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/backend/deliveries/fetch", json={
                                                        "siteId": "string",
                                                        "date": "2025-09-30"
                                                        })
    assert response.status_code == 200
    assert response.json() == {"message": "Backend challenge scaffold is running"}