from module.rates.repository import RatesRepository
from module.rates.usecase import GetAverageRateUseCase
from routers.schema import RatesRequest
from routers.schema.base_schema import Response


class RatesService:
    def __init__(self, rates_repository: RatesRepository) -> None:
        self.rates_repository = rates_repository

    def get_average_rates(self, rates_request: RatesRequest) -> Response:
        response: Response = GetAverageRateUseCase(self.rates_repository).execute(
            rates_request
        )
        return response
