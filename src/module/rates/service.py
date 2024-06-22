from src.module.rates.repository import RatesRepository
from src.module.rates.usecase import GetAverageRateUseCase
from src.routers.v1.schema import RatesRequest, Response


class RatesService:
    def __init__(self, rates_repository: RatesRepository) -> None:
        self.rates_repository = rates_repository

    def get_average_rates(self, rates_request: RatesRequest) -> Response:
        response: Response = GetAverageRateUseCase(self.rates_repository).execute(
            rates_request
        )
        return response
