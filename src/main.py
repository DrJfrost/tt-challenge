from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.config import settings
from src.database import engine, Base
from src.api.v1.api import api_router
from src.exceptions import handle_db_exceptions

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (use Alembic in prod)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Cleanup if needed
    await engine.dispose()

app = FastAPI(
    title="Project Manager API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_prod else None,
    redoc_url="/redoc" if not settings.is_prod else None,
)

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return await handle_db_exceptions(exc)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}