class WorkflowError(Exception):
    """Custom exception for workflow failures."""

class APWorkflowError(WorkflowError):
    """Specific exception for AP workflow errors."""
