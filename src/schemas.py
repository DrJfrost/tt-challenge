from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional
import uuid

# Base schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class ProjectRead(ProjectBase):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Task schemas
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    priority: int = Field(default=0, ge=0, le=100)
    completed: bool = False
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    priority: Optional[int] = Field(None, ge=0, le=100)

class TaskRead(TaskBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Pagination
class TaskListParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
