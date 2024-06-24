from abc import ABC, abstractmethod
from typing import Any

from src.routers.v1.schema import Response


class UseCase(ABC):
    @abstractmethod
    def execute(self, request: Any) -> Response:
        raise NotImplementedError
