from flask import Blueprint, current_app, jsonify, Response
from flask_pydantic import validate
from routers.schema import RatesRequest


rates = Blueprint("rates", __name__, url_prefix="/v1")


@rates.route("/rates/", methods=["GET"])
@validate(query=RatesRequest)
def fetch_cart_items(query: RatesRequest) -> Response:
    return jsonify(current_app.rates_service.get_average_rates(query).dict())
