from flask_api import status
from src.core.exceptions.rate_service_error import RateServiceError


class RequestValidationError(RateServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_400_BAD_REQUEST
    ) -> None:
        super().__init__(message, code)

    def __str__(self) -> str:
        return f"Validation Error: {self.message}"
