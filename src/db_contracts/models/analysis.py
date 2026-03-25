from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from db_contracts.base import BaseDBModel
from uuid import UUID

if TYPE_CHECKING:
    from .dependency import Service, API

class APIChange(BaseDBModel, table=True):
    __tablename__ = "api_changes"
    commit_id: str
    description: Optional[str] = None
    change_type: Optional[str] = None
    change_degree: Optional[str] = None
    api_id: UUID = Field(foreign_key="apis.id")
    api: Optional["API"] = Relationship(back_populates="changes")

class ImpactAnalysis(BaseDBModel, table=True):
    __tablename__ = "impact_analyses"
    severity: Optional[str] = None
    summary: Optional[str] = None
    api_change_id: UUID = Field(foreign_key="api_changes.id")
    api_change: Optional["APIChange"] = Relationship(back_populates="impact_analysis")

class ImpactAnalysisService(BaseDBModel, table=True):
    __tablename__ = "impact_analysis_services"
    service_id: UUID = Field(foreign_key="services.id")
    impact_analysis_id: UUID = Field(foreign_key="impact_analyses.id")
    
    service: Optional["Service"] = Relationship(back_populates="impact_analysis")
    impact_analysis: Optional["ImpactAnalysis"] = Relationship(back_populates="affected_services")