import datetime
from unittest.mock import MagicMock, patch

import pytest
from src.core.exceptions import BadRequestError
from src.module.rates.domain import RatesDTO
from src.module.rates.repository import RatesRepository
from src.module.rates.service import RatesService
from src.module.rates.usecase import GetAverageRateUseCase
from src.routers.v1.schema import RatesRequest, RatesResponse


@pytest.fixture
def mock_rates_repository() -> RatesRepository:
    return MagicMock(spec=RatesRepository)


@pytest.fixture
def rates_service(mock_rates_repository) -> RatesService:
    return RatesService(rates_repository=mock_rates_repository)


@patch.object(GetAverageRateUseCase, "execute")
def test_get_average_rates_success(mock_execute, rates_service: RatesService) -> None:
    # Create a RatesRequest object
    rates_request = RatesRequest(
        date_from=datetime.date(2023, 1, 1),
        date_to=datetime.date(2023, 1, 2),
        origin="origin_port",
        destination="destination_port",
    )

    # Create a mock response
    mock_response = RatesResponse(
        [
            RatesDTO(day="2023-01-01", average_price=100),
            RatesDTO(day="2023-01-02", average_price=200),
        ]
    )
    mock_execute.return_value = mock_response

    response = rates_service.get_average_rates(rates_request)

    assert response == mock_response
    mock_execute.assert_called_once_with(rates_request)


def test_get_average_rates_bad_request(rates_service: RatesService) -> None:
    # Create a RatesRequest object with invalid dates
    with pytest.raises(BadRequestError) as error:
        # date_from > date_to
        RatesRequest(
            date_from=datetime.date(2023, 1, 2),
            date_to=datetime.date(2023, 1, 1),
            origin="origin_port",
            destination="destination_port",
        )
    assert error.value.message == "date_to must be after date_from"
    assert error.value.status_code == 400


@pytest.mark.parametrize(
    "origin, destination, expected_error_message",
    [
        (None, "destination", "origin must be set"),
        ("Origin", "", "destination must be set"),
    ],
)
def test_get_average_rates_when_origin_or_destination_is_not_set(
    rates_service: RatesService,
    origin: str,
    destination: str,
    expected_error_message: str,
) -> None:
    # Create a RatesRequest object with invalid dates
    with pytest.raises(BadRequestError) as error:
        # date_from > date_to
        RatesRequest(
            date_from=datetime.date(2023, 1, 1),
            date_to=datetime.date(2023, 1, 10),
            origin=origin,
            destination=destination,
        )
    assert error.value.message == expected_error_message
    assert error.value.status_code == 400
