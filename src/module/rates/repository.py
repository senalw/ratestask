from abc import ABC
from datetime import date
from typing import List

from config.config import Config
from core.infra import PostgresClient
from module.rates.domain.rates_dto import Rates
from sqlalchemy import text


class RatesRepository(ABC):
    def get_rates(
        self, date_from: date, date_to: date, origin: str, destination: str
    ) -> List[Rates]:
        raise NotImplementedError


class RatesRepositoryImpl(RatesRepository):
    def __init__(self, db: PostgresClient, config: Config.ServiceConfig) -> None:
        self.db: PostgresClient = db
        self.config = config

    def get_rates(
        self, date_from: date, date_to: date, origin: str, destination: str
    ) -> List[Rates]:
        with self.db.get_session() as session:
            query = text(
                """
                WITH RECURSIVE region_tree AS (
                    SELECT slug, name, parent_slug
                    FROM regions
                    WHERE slug = :origin
                    UNION ALL
                    SELECT r.slug, r.name, r.parent_slug
                    FROM regions r
                    JOIN region_tree rt ON r.parent_slug = rt.slug
                ), origin_ports AS (
                    SELECT code
                    FROM ports
                    WHERE parent_slug = :origin OR code = :origin
                    UNION
                    SELECT p.code
                    FROM ports p
                    JOIN region_tree rt ON p.parent_slug = rt.slug
                ), destination_region_tree AS (
                    SELECT slug, name, parent_slug
                    FROM regions
                    WHERE slug = :destination
                    UNION ALL
                    SELECT r.slug, r.name, r.parent_slug
                    FROM regions r
                    JOIN destination_region_tree drt ON r.parent_slug = drt.slug
                ), destination_ports AS (
                    SELECT code
                    FROM ports
                    WHERE parent_slug = :destination OR code = :destination
                    UNION
                    SELECT p.code
                    FROM ports p
                    JOIN destination_region_tree drt ON p.parent_slug = drt.slug
                ), daily_prices AS (
                    SELECT day, AVG(price) as avg_price, COUNT(price) as price_count
                    FROM prices
                    WHERE orig_code IN (SELECT code FROM origin_ports)
                    AND dest_code IN (SELECT code FROM destination_ports)
                    AND day BETWEEN :date_from AND :date_to
                    GROUP BY day
                )
                SELECT day,
                    CASE
                        WHEN price_count >= 3 THEN avg_price
                        ELSE NULL
                    END as average_price
                FROM daily_prices
                ORDER BY day;
            """
            )

            results = session.execute(
                query,
                {
                    "date_from": date_from,
                    "date_to": date_to,
                    "origin": origin,
                    "destination": destination,
                },
            )

            return [
                Rates(
                    day=row.day.strftime(self.config.date_format),
                    average_price=round(row.average_price)
                    if row.average_price is not None
                    else None,
                )
                for row in results
            ]
