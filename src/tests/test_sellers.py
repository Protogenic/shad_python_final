import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "e_mail": "ivan.petrov@example.com",
        "password": "securepassword"
    }
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    json_data = response.json()
    
    # Check if 'id' is in response
    assert "id" in json_data
    
    # Ensure 'password' is NOT in response
    assert "password" not in json_data
    

@pytest.mark.asyncio
async def test_get_all_sellers(async_client):
    # Creating a seller before testing GET
    data = {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "e_mail": "ivan.petrov@example.com",
        "password": "securepassword"
    }
    await async_client.post("/api/v1/sellers/", json=data)

    # Now testing GET sellers
    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_delete_seller(async_client):
    # Create seller first
    data = {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "e_mail": "ivan.petrov@example.com",
        "password": "securepassword"
    }
    create_response = await async_client.post("/api/v1/sellers/", json=data)
    seller_id = create_response.json()["id"]

    # Delete the created seller
    delete_response = await async_client.delete(f"/api/v1/sellers/{seller_id}")

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT