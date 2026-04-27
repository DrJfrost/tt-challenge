from fastapi import APIRouter
from src.api.v1.endpoints import projects, tasks

api_router = APIRouter()
api_router.include_router(projects.router)
api_router.include_router(tasks.router)