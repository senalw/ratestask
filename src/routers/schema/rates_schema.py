import datetime
from typing import Any, Dict, List, Optional, Type

from core.exceptions import BadRequestError
from module.rates.domain.rates_dto import Rates
from pydantic import model_validator
from pydantic.v1 import Field
from routers.schema.base_schema import Request, Response


class RatesRequest(Request):
    date_from: Optional[datetime.date] = Field(
        default=None, description="Start date for rate query"
    )
    date_to: Optional[datetime.date] = Field(
        default=None, description="End date for rate query"
    )
    origin: str = Field(..., description="Origin location")
    destination: str = Field(..., description="Destination location")

    @model_validator(mode="before")
    @classmethod
    def set_default_dates(
        cls: Type["RatesRequest"], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not values.get("date_from"):
            values["date_from"] = datetime.date.today()
        if not values.get("date_to"):
            values["date_to"] = datetime.date.today() + datetime.timedelta(days=1)
        return values

    @model_validator(mode="before")
    @classmethod
    def check_date_order(
        cls: Type["RatesRequest"], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        date_from = values.get("date_from")
        date_to = values.get("date_to")
        if date_from and date_to and date_to < date_from:
            raise BadRequestError("date_to must be after date_from")
        return values


class RatesResponse(Response):
    rates: List[Rates]
