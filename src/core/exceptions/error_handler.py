import logging
from functools import wraps
from typing import Any, Callable

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


def handle_router_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Exception:
        try:
            return func(*args, **kwargs)
        except Exception as error:
            if isinstance(error, RateServiceError):
                raise
            logging.exception("Unknown exception", error)
            raise RateServiceError("Internal Server Error")

    return wrapper
