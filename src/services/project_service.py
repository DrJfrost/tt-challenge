from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Project, Task
from src.schemas import ProjectCreate, ProjectUpdate
from fastapi import HTTPException, status
import uuid

class ProjectService:
    @staticmethod
    async def create(db: AsyncSession, project_in: ProjectCreate) -> Project:
        project = Project(**project_in.model_dump())
        db.add(project)
        await db.flush()
        return project

    @staticmethod
    async def get(db: AsyncSession, project_id: uuid.UUID) -> Project | None:
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, project: Project, update_in: ProjectUpdate) -> Project:
        update_data = update_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        await db.flush()
        return project

    @staticmethod
    async def delete(db: AsyncSession, project: Project) -> None:
        await db.delete(project)

    @staticmethod
    async def exists(db: AsyncSession, project_id: uuid.UUID) -> bool:
        result = await db.execute(
            select(Project.id).where(Project.id == project_id).limit(1)
        )
        return result.scalar_one_or_none() is not None