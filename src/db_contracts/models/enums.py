from enum import Enum

class ValidationStatus(str, Enum):
    Passed = "passed"
    FailedRetryable = "failed_retryable"
    FailedExhausted = "failed_exhausted"

class ValidationDecision(str, Enum):
    Valid = "valid"
    Retry = "retry"
    ManualReview = "manual_review"

class FinalOutcome(str, Enum):
    Completed = "completed"
    ManualReviewRequired = "manual_review_required"


    