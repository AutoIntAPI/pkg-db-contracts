from db_contracts.models import *  # noqa: F403
from .auth import Organization, Repository
from .analysis import Change
from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, Any
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import ConfigDict
from datetime import datetime
from db_contracts.base import BaseDBModel

class Service(BaseDBModel, table=True):
    __tablename__ = "services"
    name: str
    language: Optional[str] = None
    commit_id: Optional[str] = None
    repository_id: int = Field(foreign_key="repositories.id")
    
    repository: Optional[Repository] = Relationship(back_populates="services")
    apis: list["API"] = Relationship(back_populates="service")
    api_calls_from: list["APICall"] = Relationship(
        back_populates="from_service",
        sa_relationship_kwargs={"foreign_keys": "api_calls.c.service_from_id"}
    )
    api_calls_to: list["APICall"] = Relationship(
        back_populates="to_service",
        sa_relationship_kwargs={"foreign_keys": "api_calls.c.service_to_id"}
    )

class API(BaseDBModel, table=True):
    __tablename__ = "apis"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    method: str
    path: str  # Endpoint path like "/api/users/{id}"
    file_path: str
    line_number: int
    request_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    response_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    version: Optional[str] = None
    service_id: int = Field(foreign_key="services.id")
    service: Optional[Service] = Relationship(back_populates="apis")
    changes: list["Change"] = Relationship(back_populates="api")
    api_calls: list["APICall"] = Relationship(back_populates="api")

class APICall(BaseDBModel, table=True):
    __tablename__ = "api_calls"
    file_path: str
    line_number: int
    commit_id: str

    api_id: int = Field(foreign_key="apis.id")
    api: Optional[API] = Relationship(back_populates="api_calls")
    service_from_id: int = Field(foreign_key="services.id")
    service_to_id: int = Field(foreign_key="services.id")
    
    from_service: Optional[Service] = Relationship(
        back_populates="api_calls_from",
        sa_relationship_kwargs={"foreign_keys": "api_calls.c.service_from_id"}
    )
    to_service: Optional[Service] = Relationship(
        back_populates="api_calls_to",
        sa_relationship_kwargs={"foreign_keys": "api_calls.c.service_to_id"}
    )