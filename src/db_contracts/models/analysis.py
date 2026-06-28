from sqlmodel import Field, Relationship, Column, ARRAY, TEXT
from typing import Optional, TYPE_CHECKING
from db_contracts.base import BaseDBModel
from uuid import UUID
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY, JSONB, UUID as PG_UUID
from pydantic import ConfigDict
from .enums import ValidationStatus, ValidationDecision, FinalOutcome

if TYPE_CHECKING:
    from .dependency import Repository, Service, API, APICall


class PullRequest(BaseDBModel, table=True):
    __tablename__ = "pull_requests"

    pr_number: int
    pr_title: Optional[str] = None
    head_branch: str
    base_branch: str
    repository_id: UUID = Field(foreign_key="repositories.id")
    # Lifecycle: open → merged | closed | updated
    status: str = Field(default="open")

    repository: Optional["Repository"] = Relationship(back_populates="pr_list")
    service_changes: list["ServiceChange"] = Relationship(back_populates="pr")
    api_changes: list["APIChange"] = Relationship(back_populates="pr")
    api_call_changes: list["APICallChange"] = Relationship(back_populates="pr")

    fix_records: list["FixRecord"] = Relationship(back_populates="pr")

class ServiceChange(BaseDBModel, table=True):
    __tablename__ = "service_changes"

    pr_id: UUID = Field(foreign_key="pull_requests.id")
    source_service_id: Optional[UUID] = Field(default=None, foreign_key="services.id")
    change_type: str  # added | deleted
    change_degree: Optional[str] = None  # major | minor
    name: str
    language: str
    path: str

    pr: Optional["PullRequest"] = Relationship(back_populates="service_changes")
    source_service: Optional["Service"] = Relationship(back_populates="changes")
    api_changes: list["APIChange"] = Relationship(back_populates="service_change")
    api_calls_from: list["APICallChange"] = Relationship(
        back_populates="service_from_change",
        sa_relationship_kwargs={"foreign_keys": "APICallChange.service_from_change_id"},
    )
    api_calls_to: list["APICallChange"] = Relationship(
        back_populates="service_to_change",
        sa_relationship_kwargs={"foreign_keys": "APICallChange.service_to_change_id"},
    )


class APIChange(BaseDBModel, table=True):
    __tablename__ = "api_changes"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    pr_id: UUID = Field(foreign_key="pull_requests.id")
    service_change_id: Optional[UUID] = Field(default=None, foreign_key="service_changes.id")
    api_id: UUID = Field(foreign_key="apis.id")
    description: Optional[str] = None
    change_type: Optional[str] = None
    change_degree: Optional[str] = None
    method: str
    endpoint_url: str
    file_path: str
    line_number: int
    old_request_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    new_request_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    old_response_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    new_response_schema: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    version: Optional[str] = None

    source_api: Optional["API"] = Relationship(back_populates="changes")
    pr: Optional["PullRequest"] = Relationship(back_populates="api_changes")
    service_change: Optional["ServiceChange"] = Relationship(back_populates="api_changes")
    api_call_changes: list["APICallChange"] = Relationship(back_populates="api_change")


class APICallChange(BaseDBModel, table=True):
    __tablename__ = "api_call_changes"

    pr_id: UUID = Field(foreign_key="pull_requests.id")
    source_api_call_id: Optional[UUID] = Field(default=None, foreign_key="api_calls.id")
    service_from_change_id: Optional[UUID] = Field(default=None, foreign_key="service_changes.id")
    service_to_change_id: Optional[UUID] = Field(default=None, foreign_key="service_changes.id")
    api_change_id: Optional[UUID] = Field(default=None, foreign_key="api_changes.id")
    description: Optional[str] = None
    change_type: Optional[str] = None
    change_degree: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None

    pr: Optional["PullRequest"] = Relationship(back_populates="api_call_changes")
    source_api_call: Optional["APICall"] = Relationship(back_populates="changes")
    service_from_change: Optional["ServiceChange"] = Relationship(
        back_populates="api_calls_from",
        sa_relationship_kwargs={"foreign_keys": "APICallChange.service_from_change_id"},
    )
    service_to_change: Optional["ServiceChange"] = Relationship(
        back_populates="api_calls_to",
        sa_relationship_kwargs={"foreign_keys": "APICallChange.service_to_change_id"},
    )
    api_change: Optional["APIChange"] = Relationship(back_populates="api_call_changes")

class FixRecord(BaseDBModel, table=True):
    __tablename__ = "fix_records"
    run_id: UUID
    pr_id: UUID = Field(foreign_key="pull_requests.id")
    downstream_services_ids: Optional[list[UUID]] = Field(
        default=None, sa_column=Column(PG_ARRAY(PG_UUID(as_uuid=True)))
    )
    validation_status: ValidationStatus
    validation_decision: ValidationDecision
    schema_validation_passed: Optional[bool] = None
    schema_validation_errors: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(TEXT)))
    static_analysis_passed: Optional[bool] = None
    static_analysis_errors: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(TEXT)))
    syntax_check_passed: Optional[bool] = None
    syntax_check_errors: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(TEXT)))
    confidence_score: Optional[float] = None
    generated_patch: Optional[str] = None
    formatted_patch: Optional[str] = None
    patch_explanation: Optional[str] = None
    semantic_validation_ran: bool
    semantic_validation_passed: Optional[bool] = None
    semantic_validation_notes: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(TEXT)))
    semantic_validation_score: Optional[float] = None
    branch_name: Optional[str] = None
    retry_count: Optional[int] = None
    final_outcome: Optional[FinalOutcome] = None

    pr: Optional["PullRequest"] = Relationship(back_populates="fix_records")
