import datetime
from typing import Any, List, Optional

from core.exceptions import BadRequestError
from module.rates.domain.rates_dto import Rates
from pydantic import field_validator
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

    # @validator("date_from", pre=True, always=True)
    @field_validator("date_from")
    def set_default_date(cls, v: Any) -> datetime.datetime:
        if v is None:
            today = datetime.datetime.combine(
                datetime.date.today(), datetime.time(0, 0, 1)
            )
            return today
        return v

    @field_validator("date_to")
    def set_default_date_to(cls, v: Any) -> datetime.datetime:
        if v is None:
            today = datetime.datetime.combine(
                datetime.date.today(), datetime.time(23, 59, 59)
            )
            return today
        return v

    @field_validator("date_to")
    def check_date_order(cls, v: Any, values: Any) -> datetime.datetime:
        if "date_from" in values.data.keys() and v < values.data["date_from"]:
            raise BadRequestError("date_to must be after date_from")
        return v


class RatesResponse(Response):
    rates: List[Rates]
