from typing import Dict

from flask_api import status


class RateServiceError(Exception):
    def __init__(
        self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, int]:
        return {"error": str(self), "status_code": self.status_code}
