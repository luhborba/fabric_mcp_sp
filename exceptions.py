class FabricMCPError(Exception):
    """Base exception para fabric-mcp."""
    code: str = "FABRIC_ERROR"

    def __init__(self, message: str, details: str = "", suggestion: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details
        self.suggestion = suggestion

    def to_dict(self) -> dict:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "suggestion": self.suggestion,
            },
        }


class AuthError(FabricMCPError):
    code = "AUTH_ERROR"


class NotFoundError(FabricMCPError):
    code = "NOT_FOUND"


class PermissionError(FabricMCPError):
    code = "PERMISSION_DENIED"


class ValidationError(FabricMCPError):
    code = "VALIDATION_ERROR"


class RateLimitError(FabricMCPError):
    code = "RATE_LIMIT"


class OperationTimeoutError(FabricMCPError):
    code = "OPERATION_TIMEOUT"


class FabricAPIError(FabricMCPError):
    code = "FABRIC_API_ERROR"
