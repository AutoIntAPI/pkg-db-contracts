from db_contracts.models import *  # noqa: F403
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, Any
from sqlalchemy.dialects.postgresql import JSONB
from .dependency import Service
from db_contracts.base import BaseDBModel

class Organization(BaseDBModel, table=True):
    __tablename__ = "organizations"
    
    name: str
    repositories: list["Repository"] = Relationship(back_populates="organization")

class Repository(BaseDBModel, table=True):
    __tablename__ = "repositories"
    
    name: str
    url: str
    organization_id: int = Field(foreign_key="organizations.id")
    
    organization: Optional[Organization] = Relationship(back_populates="repositories")
    services: list["Service"] = Relationship(back_populates="repository")
