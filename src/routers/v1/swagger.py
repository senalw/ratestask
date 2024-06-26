import json

from flask import jsonify, Response
from flask_swagger_ui import get_swaggerui_blueprint
from settings import ROOT_DIR

SWAGGER_URL = "/swagger"
API_URL = "swagger.json"
swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)


@swagger_ui.route("/swagger.json")
def swagger() -> Response:
    with open(f"{ROOT_DIR}/resources/swagger.json", "r") as f:
        return jsonify(json.load(f))
