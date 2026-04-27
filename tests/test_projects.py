import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    payload = {"name": "Test Project", "description": "A test"}
    response = await client.post("/api/v1/projects/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_project_not_found(client: AsyncClient):
    fake_id = uuid.uuid4()
    response = await client.get(f"/api/v1/projects/{fake_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    # Create first
    payload = {"name": "Original", "description": "Desc"}
    create_resp = await client.post("/api/v1/projects/", json=payload)
    project_id = create_resp.json()["id"]
    
    # Update
    update_payload = {"name": "Updated"}
    response = await client.put(f"/api/v1/projects/{project_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):
    payload = {"name": "To Delete"}
    create_resp = await client.post("/api/v1/projects/", json=payload)
    project_id = create_resp.json()["id"]
    
    response = await client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_resp = await client.get(f"/api/v1/projects/{project_id}")
    assert get_resp.status_code == 404