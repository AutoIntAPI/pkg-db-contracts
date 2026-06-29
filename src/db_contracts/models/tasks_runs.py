from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, Any
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import ConfigDict
from datetime import datetime
from db_contracts.base import BaseDBModel

class AITask(BaseDBModel, table=True):
    """Track async AI processing tasks"""
    __tablename__ = "ai_tasks"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    task_id: str = Field(unique=True, index=True)  # from AI provider
    service_name: str  # which service being analyzed
    model_name: str  # AI model used
    status: str = Field(default="pending")  # pending, completed, failed
    result: Optional[dict] = Field(default=None, sa_column=Column(JSONB))  # AI response
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Store analysis context for processing result later
    organization_name: str
    repository_path: str
    repository_url: str  # Original GitHub URL
    all_service_names: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    service_files: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
   

class DependencyAnalysisRun(BaseDBModel, table=True):
    __tablename__ = "dependency_analysis_runs"

    analysis_id: str = Field(index=True, unique=True)
    project_id: str = Field(index=True)
    callback_url: str
    status: str = Field(default="pending", index=True)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    summary: dict[str, Any] | None = Field(default=None, sa_column=Column(JSONB))
    result: dict[str, Any] | None = Field(default=None, sa_column=Column(JSONB))
    error: dict[str, Any] | None = Field(default=None, sa_column=Column(JSONB))
    callback_delivery_error: str | None = None
    callback_attempted_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DependencyAnalysisTaskLink(BaseDBModel, table=True):
    __tablename__ = "dependency_analysis_task_links"

    analysis_id: str = Field(index=True)
    task_id: str = Field(index=True, unique=True)
    service_name: str
    repository_url: str
    created_at: datetime = Field(default_factory=datetime.now)
