from flask_api import status
from src.core.exceptions.rate_service_error import RateServiceError


class AlreadyExistsError(RateServiceError):
    def __init__(self, message: str, code: status = status.HTTP_409_CONFLICT) -> None:
        super().__init__(message, code)

    def __str__(self) -> str:
        return f"Resource Already Exists: {self.message}"
