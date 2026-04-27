from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas import TaskCreate, TaskUpdate, TaskRead, TaskListParams
from src.services.task_service import TaskService
from src.dependencies import verify_api_key
import uuid

router = APIRouter(tags=["tasks"])

@router.post("/projects/{project_id}/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def create_task(
    project_id: uuid.UUID, 
    task_in: TaskCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await TaskService.create(db, project_id, task_in)

@router.get("/projects/{project_id}/tasks/", response_model=list[TaskRead], dependencies=[Depends(verify_api_key)])
async def list_tasks(
    project_id: uuid.UUID,
    params: TaskListParams = Depends(),
    db: AsyncSession = Depends(get_db)
):
    tasks, _ = await TaskService.get_by_project(db, project_id, params)
    # Bonus: Add pagination headers if needed
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskRead, dependencies=[Depends(verify_api_key)])
async def update_task(
    task_id: uuid.UUID, 
    task_in: TaskUpdate, 
    db: AsyncSession = Depends(get_db)
):
    task = await TaskService.get(db, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    return await TaskService.update(db, task, task_in)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    task = await TaskService.get(db, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    await TaskService.delete(db, task)