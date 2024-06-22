from flask import Blueprint, current_app, jsonify, Response
from flask_pydantic import validate
from src.core.exceptions.error_handler import handle_router_errors
from src.routers.v1.schema import RatesRequest


rates = Blueprint("rates", __name__, url_prefix="/v1")


@rates.route("/rates/", methods=["GET"])
@validate(query=RatesRequest)
@handle_router_errors
def fetch_average_rates(query: RatesRequest) -> Response:
    return jsonify(current_app.rates_service.get_average_rates(query).dict())
