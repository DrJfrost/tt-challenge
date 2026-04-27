from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate, TaskListParams
from fastapi import HTTPException, status
from src.services.project_service import ProjectService
import uuid

class TaskService:
    @staticmethod
    async def create(db: AsyncSession, project_id: uuid.UUID, task_in: TaskCreate) -> Task:
        if not await ProjectService.exists(db, project_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
        
        task = Task(project_id=project_id, **task_in.model_dump())
        db.add(task)
        await db.flush()
        return task

    @staticmethod
    async def get_by_project(
        db: AsyncSession, 
        project_id: uuid.UUID, 
        params: TaskListParams
    ) -> tuple[list[Task], int]:
        # Optimized query with pagination + sorting
        query = select(Task).where(Task.project_id == project_id).order_by(Task.priority.desc())
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # Apply pagination
        query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        return tasks, total

    @staticmethod
    async def get(db: AsyncSession, task_id: uuid.UUID) -> Task | None:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, task: Task, update_in: TaskUpdate) -> Task:
        update_data = update_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await db.flush()
        return task

    @staticmethod
    async def delete(db: AsyncSession, task: Task) -> None:
        await db.delete(task)