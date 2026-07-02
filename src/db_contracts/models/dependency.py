from sqlmodel import Field, Relationship, Column, SQLModel
from typing import Optional, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import ConfigDict
from db_contracts.base import BaseDBModel
from uuid import UUID
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .analysis import PullRequest, ServiceChange, APIChange, APICallChange

class Repository(BaseDBModel, table=True):
    __tablename__ = "repositories"

    name: str
    url: str
    default_branch: Optional[str] = None

    services: list["Service"] = Relationship(back_populates="repository")
    pr_list: list["PullRequest"] = Relationship(back_populates="repository")


class ProjectRepository(SQLModel, table=True):
    __tablename__ = "project_repositories"

    project_id: UUID = Field(primary_key=True)
    repository_id: UUID = Field(primary_key=True, foreign_key="repositories.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

class Service(BaseDBModel, table=True):
    __tablename__ = "services"
    name: str
    language: str
    repository_id: UUID = Field(foreign_key="repositories.id")
    path: str
    
    repository: Optional["Repository"] = Relationship(back_populates="services")
    apis: list["API"] = Relationship(back_populates="service")
    api_calls_from: list["APICall"] = Relationship(
        back_populates="service_from",
        sa_relationship_kwargs={"foreign_keys": "APICall.service_from_id"}
    )
    api_calls_to: list["APICall"] = Relationship(
        back_populates="service_to",
        sa_relationship_kwargs={"foreign_keys": "APICall.service_to_id"}
    )
    changes: list["ServiceChange"] = Relationship(back_populates="source_service")

class API(BaseDBModel, table=True):
    __tablename__ = "apis"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    method: str
    endpoint_url: str  # Endpoint path like "/api/users/{id}"
    file_path: str
    line_number: int
    request_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    response_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    version: Optional[str] = None
    # Typed path-parameter metadata emitted by the endpoint-extraction AI.
    # Schema: {"params": [{"name": str, "position": int, "type": str, "aliases": list[str]}]}
    path_params_meta: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    service_id: UUID = Field(foreign_key="services.id")
    service: Optional["Service"] = Relationship(back_populates="apis")
    changes: list["APIChange"] = Relationship(back_populates="source_api")
    api_calls: list["APICall"] = Relationship(back_populates="api")

class APICall(BaseDBModel, table=True):
    __tablename__ = "api_calls"
    file_path: str
    line_number: int

    api_id: UUID = Field(foreign_key="apis.id")
    api: Optional["API"] = Relationship(back_populates="api_calls")
    service_from_id: UUID = Field(foreign_key="services.id")
    service_to_id: UUID = Field(foreign_key="services.id")
    
    service_from: Optional["Service"] = Relationship(
        back_populates="api_calls_from",
        sa_relationship_kwargs={"foreign_keys": "APICall.service_from_id"}
    )
    service_to: Optional["Service"] = Relationship(
        back_populates="api_calls_to",
        sa_relationship_kwargs={"foreign_keys": "APICall.service_to_id"}
    )
    changes: list["APICallChange"] = Relationship(back_populates="source_api_call")
