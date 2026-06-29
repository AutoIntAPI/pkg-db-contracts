"""Import all models so metadata is fully populated for migrations."""

from .tasks_runs import *
from .analysis import *
from .dependency import *


__all__ = [
    "AITask",
    "Repository",
    "ProjectRepository",
    "Service",
    "API",
    "APICall",
    "PullRequest",
    "ServiceChange",
    "APIChange",
    "APICallChange",
    "FixRecord",
    "DependencyAnalysisRun",
    "DependencyAnalysisTaskLink",
]
