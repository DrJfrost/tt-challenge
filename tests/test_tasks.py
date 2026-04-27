import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    # Create project first
    proj_resp = await client.post("/api/v1/projects/", json={"name": "Task Test"})
    project_id = proj_resp.json()["id"]
    
    payload = {"title": "Test Task", "priority": 10, "completed": False}
    response = await client.post(f"/api/v1/projects/{project_id}/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == 10

@pytest.mark.asyncio
async def test_list_tasks_sorted_by_priority(client: AsyncClient):
    proj_resp = await client.post("/api/v1/projects/", json={"name": "Sort Test"})
    project_id = proj_resp.json()["id"]
    
    # Create tasks with different priorities
    for priority in [5, 20, 10]:
        await client.post(
            f"/api/v1/projects/{project_id}/tasks/",
            json={"title": f"Priority {priority}", "priority": priority}
        )
    
    response = await client.get(f"/api/v1/projects/{project_id}/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    priorities = [t["priority"] for t in tasks]
    assert priorities == sorted(priorities, reverse=True)

@pytest.mark.asyncio
async def test_task_not_found(client: AsyncClient):
    fake_id = uuid.uuid4()
    response = await client.put(f"/api/v1/tasks/{fake_id}", json={"title": "X"})
    assert response.status_code == 404