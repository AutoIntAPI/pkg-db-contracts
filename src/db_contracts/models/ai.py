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
   