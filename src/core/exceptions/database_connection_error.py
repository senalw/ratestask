from flask_api import status
from src.core.exceptions.rate_service_error import RateServiceError


class DatabaseConnectionError(RateServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_503_SERVICE_UNAVAILABLE
    ) -> None:
        super().__init__(message, code)

    def __str__(self) -> str:
        return f"Database Connection Error: {self.message}"
