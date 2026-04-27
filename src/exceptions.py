from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

async def handle_db_exceptions(exc: Exception):
    if isinstance(exc.__cause__, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation",
        )
    raise exc