from unittest.mock import MagicMock

import pytest
from flask import current_app, Flask
from src.core.exceptions import BadRequestError
from src.routers.v1.rate import rates


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(rates)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_rates_service(app):
    with app.app_context():
        mock_service = MagicMock()
        current_app.rates_service = mock_service
        yield mock_service


def test_fetch_average_rates_valid_request(client, mock_rates_service):
    # Mock the rates_service response
    mock_response = MagicMock()
    mock_response.dict.return_value = {
        "rates": [
            {"day": "2024-06-01", "average_price": 1000},
            {"day": "2024-06-02", "average_price": 1100},
        ]
    }
    mock_rates_service.get_average_rates.return_value = mock_response

    # Define the query parameters
    query_params = {
        "date_from": "2024-06-01",
        "date_to": "2024-06-02",
        "origin": "GBGOO",
        "destination": "NOTAE",
    }

    # Make the GET request
    response = client.get("/v1/rates/", query_string=query_params)

    # Assert the response
    assert response.status_code == 200
    assert response.json == mock_response.dict.return_value


def test_fetch_average_rates_invalid_date_range(client, mock_rates_service):
    # Define the query parameters with invalid date range
    query_params = {
        "date_from": "2024-06-03",
        "date_to": "2024-06-02",
        "origin": "GBGOO",
        "destination": "NOTAE",
    }

    # Make the GET request
    with pytest.raises(BadRequestError) as error:
        client.get("/v1/rates/", query_string=query_params)

    # Assert the response
    assert error.value.status_code == 400
    assert error.value.message == "date_to must be after date_from"


def test_fetch_average_rates_missing_origin(client, mock_rates_service):
    # Define the query parameters with missing origin
    query_params = {
        "date_from": "2024-06-01",
        "date_to": "2024-06-02",
        "destination": "NOTAE",
    }

    # Make the GET request
    with pytest.raises(BadRequestError) as error:
        client.get("/v1/rates/", query_string=query_params)

    # Assert the response
    assert error.value.status_code == 400
    assert error.value.message == "origin must be set"


def test_fetch_average_rates_missing_destination(client, mock_rates_service):
    # Define the query parameters with missing destination
    query_params = {
        "date_from": "2024-06-01",
        "date_to": "2024-06-02",
        "origin": "GBGOO",
    }

    # Make the GET request
    with pytest.raises(BadRequestError) as error:
        client.get("/v1/rates/", query_string=query_params)

    # Assert the response
    assert error.value.status_code == 400
    assert error.value.message == "destination must be set"
