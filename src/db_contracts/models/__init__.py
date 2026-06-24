"""Import all models so metadata is fully populated for migrations."""

from .ai import *
from .analysis import *
from .dependency import *


__all__ = [
    "AITask",
    "Project",
    "Repository",
    "Service",
    "API",
    "APICall",
    "PullRequest",
    "ServiceChange",
    "APIChange",
    "APICallChange",
    "FixRecord",
]
