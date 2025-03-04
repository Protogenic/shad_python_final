import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "e_mail": "ivan@mail.com",
        "password": "qwerty123"
    }
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["first_name"] == "Ivan"


@pytest.mark.asyncio
async def test_get_all_sellers(async_client):
    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_delete_seller(async_client):
    response = await async_client.delete("/api/v1/sellers/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
