"""Import all models so metadata is fully populated for migrations."""

from .ai import *
from .analysis import *
from .auth import *
from .dependency import *
# from .fixgen import FixSuggestion


__all__ = [
    "API",
    "APICall",
    # "ApiSchema",
    # "AnalysisRun",
    # "BreakingChange",
    # "FixSuggestion",
    "AITask",
    "Organization",
    "Project",
    "Repository",
    "Service",
    "User",
    "UserProject",
    # "UserOrganization",
    "APIChange",
]
