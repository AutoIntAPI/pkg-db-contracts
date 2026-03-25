from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from db_contracts.base import BaseDBModel
from uuid import UUID
from datetime import datetime

if TYPE_CHECKING:
    from .analysis import APIChange, ImpactAnalysis
    from .dependency import Service

class Organization(BaseDBModel, table=True):
    __tablename__ = "organizations"
    
    name: str
    projects: list["Project"] = Relationship(back_populates="organization")

class Project(BaseDBModel, table=True):
    __tablename__ = "projects"

    name: str
    description: Optional[str] = None
    status: Optional[str] = None  # e.g., "active", "archived"
    organization_id: UUID = Field(foreign_key="organizations.id")

    organization: Optional[Organization] = Relationship(back_populates="projects")
    repositories: list["Repository"] = Relationship(back_populates="project")

class Repository(BaseDBModel, table=True):
    __tablename__ = "repositories"
    
    name: str
    url: str
    project_id: UUID = Field(foreign_key="projects.id")

    project: Optional[Project] = Relationship(back_populates="repositories")
    services: list["Service"] = Relationship(back_populates="repository")

class User(BaseDBModel, table=True):
    __tablename__ = "users"
    
    name: str
    email: str
    role: Optional[str] = None  # e.g., "admin", "developer",
    organization_id: UUID = Field(foreign_key="organizations.id")
    organization: Optional[Organization] = Relationship(back_populates="users")

class UserProject(SQLModel, table=True):
    __tablename__ = "user_projects"
    
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    project_id: UUID = Field(foreign_key="projects.id", primary_key=True)

class Notification(BaseDBModel, table=True):
    __tablename__ = "notifications"
    
    message: str
    impact_analysis_id: UUID = Field(foreign_key="impact_analyses.id")
    impact_analysis: Optional["ImpactAnalysis"] = Relationship(back_populates="notifications")
    api_change_id: UUID = Field(foreign_key="api_changes.id")
    api_change: Optional["APIChange"] = Relationship(back_populates="notifications")
    recipient_id: UUID = Field(foreign_key="users.id")
    recipient: Optional[User] = Relationship(back_populates="notifications")
    channel: Optional[str] = None  # e.g., "email", "slack"
    status: Optional[str] = None  # e.g., "sent", "pending", "failed"
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None