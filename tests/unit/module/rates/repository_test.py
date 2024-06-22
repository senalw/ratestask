from datetime import date
from unittest.mock import MagicMock

import pytest
from src.config.config import Config
from src.core.infra import PostgresClient
from src.module.rates.domain.rates_dto import RatesDTO
from src.module.rates.repository import RatesRepositoryImpl


@pytest.fixture
def mock_db() -> PostgresClient:
    return MagicMock(spec=PostgresClient)


@pytest.fixture
def mock_config() -> Config.AppConfig:
    config = MagicMock(spec=Config.AppConfig)
    config.date_format = "%Y-%m-%d"
    return config


@pytest.fixture
def rates_repository(
    mock_db: PostgresClient, mock_config: Config.AppConfig
) -> RatesRepositoryImpl:
    return RatesRepositoryImpl(db=mock_db, config=mock_config)


def test_get_rates_success(
    rates_repository: RatesRepositoryImpl,
    mock_db: PostgresClient,
    mock_config: Config.AppConfig,
) -> None:
    # Mock session and query results
    mock_session = MagicMock()
    mock_db.get_session.return_value.__enter__.return_value = mock_session

    mock_result = [
        MagicMock(day=date(2023, 1, 1), average_price=100.0, price_count=3),
        MagicMock(day=date(2023, 1, 2), average_price=None, price_count=2),
    ]
    mock_session.execute.return_value = mock_result

    date_from = date(2023, 1, 1)
    date_to = date(2023, 1, 2)
    origin = "origin_port"
    destination = "destination_port"

    rates = rates_repository.get_rates(date_from, date_to, origin, destination)

    expected_rates = [
        RatesDTO(day="2023-01-01", average_price=100),
        RatesDTO(day="2023-01-02", average_price=None),
    ]

    assert rates == expected_rates
    mock_db.get_session.assert_called_once()
    mock_session.execute.assert_called_once()


def test_get_rates_empty_result(
    rates_repository: RatesRepositoryImpl,
    mock_db: PostgresClient,
    mock_config: Config.AppConfig,
) -> None:
    # Mock session and empty query results
    mock_session = MagicMock()
    mock_db.get_session.return_value.__enter__.return_value = mock_session

    mock_result = []
    mock_session.execute.return_value = mock_result

    date_from = date(2023, 1, 1)
    date_to = date(2023, 1, 2)
    origin = "origin_port"
    destination = "destination_port"

    rates = rates_repository.get_rates(date_from, date_to, origin, destination)

    assert rates == []
    mock_db.get_session.assert_called_once()
    mock_session.execute.assert_called_once()
