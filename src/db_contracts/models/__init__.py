"""Import all models so metadata is fully populated for migrations."""

from .ai import *
from .analysis import *
from .auth import *
from .dependency import *
# from .fixgen import FixSuggestion


__all__ = [
    "API",
    "APICall",
    "AITask",
    "Organization",
    "Project",
    "Repository",
    "Service",
    "User",
    "UserProject",
    "APIChange",
    "ImpactAnalysis",
    "ImpactAnalysisService",
    "Notification",
]
