from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas import ProjectCreate, ProjectUpdate, ProjectRead
from src.services.project_service import ProjectService
from src.dependencies import verify_api_key
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await ProjectService.create(db, project_in)

@router.get("/{project_id}", response_model=ProjectRead, dependencies=[Depends(verify_api_key)])
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.get(db, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectRead, dependencies=[Depends(verify_api_key)])
async def update_project(
    project_id: uuid.UUID, 
    project_in: ProjectUpdate, 
    db: AsyncSession = Depends(get_db)
):
    project = await ProjectService.get(db, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return await ProjectService.update(db, project, project_in)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
async def delete_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    project = await ProjectService.get(db, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    await ProjectService.delete(db, project)