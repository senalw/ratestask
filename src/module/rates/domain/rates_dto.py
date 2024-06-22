from dataclasses import dataclass


@dataclass
class RatesDTO:
    day: str
    average_price: int
