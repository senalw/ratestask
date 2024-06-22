from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from src.config.config import Config
from src.core.exceptions import (
    AlreadyExistsError,
    DatabaseConnectionError,
    RateServiceError,
)
from src.core.infra.database import PostgresClient


@pytest.fixture
def db_config() -> Config:
    config = Config()
    config.db_configs.db_url = (
        "postgresql+psycopg2://ratestask:ratestask@db:5432/rates-service"
    )
    return config


@pytest.fixture
def postgres_client(db_config) -> PostgresClient:
    return PostgresClient(db_config)


def test_get_session_success(postgres_client) -> None:
    with patch(
        "src.core.infra.database.postgres_client.sessionmaker"
    ) as mock_sessionmaker:
        mock_session = MagicMock()
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)

        with postgres_client.get_session() as session:
            assert session == mock_session


def test_get_session_integrity_error(postgres_client) -> None:
    with patch(
        "src.core.infra.database.postgres_client.sessionmaker"
    ) as mock_sessionmaker:
        mock_session = MagicMock()
        mock_session.commit.side_effect = IntegrityError("", "", "")
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)

        with pytest.raises(AlreadyExistsError) as exec_info:
            with postgres_client.get_session():
                pass
        assert exec_info.value.status_code == 409


def test_get_session_operational_error(postgres_client) -> None:
    with patch(
        "src.core.infra.database.postgres_client.sessionmaker"
    ) as mock_sessionmaker:
        mock_session = MagicMock()
        mock_session.commit.side_effect = OperationalError("", "", "")
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)

        with pytest.raises(DatabaseConnectionError) as exec_info:
            with postgres_client.get_session():
                pass
        assert exec_info.value.status_code == 503


def test_get_session_programming_error(postgres_client) -> None:
    with patch(
        "src.core.infra.database.postgres_client.sessionmaker"
    ) as mock_sessionmaker:
        mock_session = MagicMock()
        mock_session.commit.side_effect = ProgrammingError("", "", "")
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)

        with pytest.raises(DatabaseConnectionError) as exec_info:
            with postgres_client.get_session():
                pass
        assert exec_info.value.status_code == 503


def test_get_session_unknown_error(postgres_client) -> None:
    with patch(
        "src.core.infra.database.postgres_client.sessionmaker"
    ) as mock_sessionmaker:
        mock_session = MagicMock()
        mock_session.commit.side_effect = Exception("Unknown error")
        mock_sessionmaker.return_value = MagicMock(return_value=mock_session)

        with pytest.raises(RateServiceError) as exec_info:
            with postgres_client.get_session():
                pass
        assert exec_info.value.status_code == 500
