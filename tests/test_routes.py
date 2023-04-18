import httpx
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from main import app
from os import environ
from app.schemas import (
    AuthorSchemaIn,
)

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_root():
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/")
        assert response.status_code == 200


# Example:
@pytest.mark.asyncio
async def test_create_author():
    new_author = AuthorSchemaIn(name="Test Author")
    async with httpx.AsyncClient(app=app, base_url=BASE_URL) as client:
        headers = {"Authorization": environ.get("TOKEN")}
        response = await client.post("/author", json=new_author.dict(), headers=headers)
        assert response.status_code == 201
        assert response.json()["name"] == new_author.name
