from typing import Any, List

from module.rates.domain.rates_dto import Rates
from module.rates.repository import RatesRepository
from module.usecase import UseCase
from routers.schema.rates_schema import RatesResponse


class GetAverageRateUseCase(UseCase):
    def __init__(self, rates_repo: RatesRepository) -> None:
        self.rates_repo = rates_repo

    def execute(self, request: Any) -> Any:
        rates: List[Rates] = self.rates_repo.get_rates(
            request.date_from,
            request.date_to,
            request.origin,
            request.destination,
        )

        return RatesResponse(rates=rates)
