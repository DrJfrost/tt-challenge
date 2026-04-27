from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from src.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    __table_args__ = (Index("idx_projects_name", "name"),)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    priority = Column(Integer, default=0, index=True)  # Higher = higher priority
    completed = Column(Boolean, default=False)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    
    __table_args__ = (
        Index("idx_tasks_project_priority", "project_id", "priority"),
    )
