from db_contracts.models import *  # noqa: F403
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .dependency import API
from db_contracts.base import BaseDBModel

class Change(BaseDBModel, table=True):
    __tablename__ = "changes"
    id: Optional[int] = Field(default=None, primary_key=True)
    commit_id: str
    description: Optional[str] = None
    type_of_change: Optional[str] = None
    degree_of_change: Optional[str] = None
    api_id: int = Field(foreign_key="apis.id")
    api: Optional["API"] = Relationship(back_populates="changes")