from typing import Any, List

from src.module.rates.domain.rates_dto import RatesDTO
from src.module.rates.repository import RatesRepository
from src.module.usecase import UseCase
from src.routers.v1.schema import Response
from src.routers.v1.schema.rates_schema import RatesResponse


class GetAverageRateUseCase(UseCase):
    def __init__(self, rates_repo: RatesRepository) -> None:
        self.rates_repo = rates_repo

    def execute(self, request: Any) -> Response:
        rates: List[RatesDTO] = self.rates_repo.get_rates(
            request.date_from,
            request.date_to,
            request.origin,
            request.destination,
        )
        return RatesResponse.model_validate(rates)
