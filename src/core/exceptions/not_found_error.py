from flask_api import status
from src.core.exceptions.rate_service_error import RateServiceError


class NotFoundError(RateServiceError):
    def __init__(self, message: str, code: status = status.HTTP_404_NOT_FOUND) -> None:
        super().__init__(message, code)

    def __str__(self) -> str:
        return f"Not Found Error: {self.message}"
