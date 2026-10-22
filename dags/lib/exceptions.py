class DataQualityError(Exception):
    """Raised when data quality gates fail, such as missing primary data."""
    pass

class DepartmentLookupError(Exception):
    """Raised when department resolution or lookup fails."""
    pass

class ReportGenerationError(Exception):
    """Raised when PDF or Excel artifact generation fails."""
    pass

class ArtifactValidationError(Exception):
    """Raised when generated artifacts are missing or empty."""
    pass

class SMTPError(Exception):
    """Raised when SMTP connection or email delivery fails."""
    pass

class DeliveryInProgressError(Exception):
    """Raised when a delivery is already in SENDING state."""
    pass

class AlreadySentError(Exception):
    """Raised when a delivery is already in SUCCESS state."""
    pass

class UnexpectedError(Exception):
    """Raised for any unexpected or unclassified failure."""
    pass
