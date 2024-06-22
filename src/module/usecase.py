from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.routers.v1.schema import Response


@dataclass
class UseCase(ABC):
    @abstractmethod
    def execute(self, request: Any) -> Response:
        raise NotImplementedError
