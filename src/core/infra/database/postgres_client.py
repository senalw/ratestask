import logging
from contextlib import contextmanager

from flask_api import status
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session, sessionmaker
from src.config.config import Config
from src.core.exceptions import (
    AlreadyExistsError,
    DatabaseConnectionError,
    RateServiceError,
)


class PostgresClient:
    def __init__(self, configs: Config) -> None:
        self.db_engine: Engine = create_engine(configs.db_configs.db_url)

    @contextmanager
    def get_session(self) -> Session:
        session = None
        try:
            # "auto flush" should be turned off for merging objects in a same session.
            sm = sessionmaker(bind=self.db_engine, autoflush=False)
            session = sm()
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            self._handle_db_errors(e)
        finally:
            if session:
                session.flush()
                session.close()

    @staticmethod
    def _handle_db_errors(throwable: Exception) -> None:
        logging.exception(throwable)

        if isinstance(throwable, RateServiceError):
            raise throwable
        elif isinstance(
            throwable, (OperationalError, ProgrammingError)
        ):  # Programming error occurs when table not found
            raise DatabaseConnectionError("Unable to connect to the database")
        elif isinstance(throwable, IntegrityError):  # db constraint error
            raise AlreadyExistsError("Resource already exists")
        else:
            raise RateServiceError(
                "Unknown Error", status.HTTP_500_INTERNAL_SERVER_ERROR
            )
