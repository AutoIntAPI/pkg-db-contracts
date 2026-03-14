"""Import all models so metadata is fully populated for migrations."""

from .ai import LlmTask
from .analysis import AnalysisRun, BreakingChange
from .auth import Organization, Repo, User, UserOrganization
from .dependency import Api, ApiCall, ApiSchema, Service
from .fixgen import FixSuggestion

__all__ = [
    "Api",
    "ApiCall",
    "ApiSchema",
    "AnalysisRun",
    "BreakingChange",
    "FixSuggestion",
    "LlmTask",
    "Organization",
    "Repo",
    "Service",
    "User",
    "UserOrganization",
]
