from config.config import Config
from core.exceptions.error_handler import register_error_handlers
from core.infra import PostgresClient
from flask import Flask
from module.rates.repository import RatesRepository, RatesRepositoryImpl
from module.rates.service import RatesService
from src.routers.v1 import rate, swagger


def initialize_services(app: Flask) -> None:
    db: PostgresClient = PostgresClient(app.configs)
    rates_repository: RatesRepository = RatesRepositoryImpl(
        db, app.configs.service_config
    )
    app.rates_service: RatesService = RatesService(rates_repository)


if __name__ == "__main__":
    app: Flask = Flask(__name__)
    app.register_blueprint(rate.rates)
    app.register_blueprint(swagger.swagger_ui)
    register_error_handlers(app)

    configs: Config = Config()
    app.configs = configs
    initialize_services(app)

    app.run(host="0.0.0.0", port=configs.app_config.port)  # noqa S104
