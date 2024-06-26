import logging
from configparser import ConfigParser
from typing import List

from settings import ROOT_DIR
from src.config.env_interpolation import EnvInterpolation


class Config:
    def __init__(self) -> None:
        config_parser: ConfigParser = ConfigParser(interpolation=EnvInterpolation())
        config_parser.read(f"{ROOT_DIR}/resources/config.ini")
        self.db_configs: Config.DatabaseConfig = Config.DatabaseConfig(
            config_parser
        )  # noqa E501
        self.app_config: Config.AppConfig = Config.AppConfig(config_parser)  # noqa E501

        missing_configs: List[str] = self.__validate_configs()
        if missing_configs:
            logging.error(f"Missing Configs: {missing_configs}")

    def __validate_configs(self) -> List[str]:
        missing_configs = []
        if not self.db_configs.db_url:
            missing_configs.append("DB_URL")
        if not self.app_config.port:
            missing_configs.append("PORT")
        if not self.app_config.date_format:
            missing_configs.append("DATE_FORMAT")

        return missing_configs

    class DatabaseConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.db_url: str = configs.get("Database", "DB_URL")

    class AppConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.port: int = configs.getint("APP", "PORT")
            self.date_format = configs.get("APP", "DATE_FORMAT")
