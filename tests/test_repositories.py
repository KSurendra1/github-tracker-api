import pytest
from httpx import AsyncClient
from app.main import app

# Use ASGI transport for compatibility across httpx versions
try:
    from httpx import ASGITransport
except ImportError:  # older httpx may keep transports in a private module
    from httpx._transports.asgi import ASGITransport

@pytest.mark.asyncio
async def test_create_repo():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/repositories/", json={
            "owner": "fastapi",
            "repo_name": "fastapi"
        })
    assert response.status_code == 201
