from dataclasses import dataclass
from typing import Optional


@dataclass
class RatesDTO:
    day: str
    average_price: Optional[int]
