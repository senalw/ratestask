from typing import Any

from flask import Flask, jsonify, Response
from src.core.exceptions import RateServiceError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(Exception)
    def handle_generic_error(error: Any) -> Response:
        if isinstance(error, RateServiceError):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response
        # Default 500 error handling for other exceptions
        response = jsonify({"error": "Internal Server Error", "status_code": 500})
        response.status_code = 500
        return response
