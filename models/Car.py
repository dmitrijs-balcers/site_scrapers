from dataclasses import dataclass
from typing import NamedTuple

CarDate = NamedTuple("CarDate", [("month", str), ("year", str)])


@dataclass
class Car:
    url: str
    previewImgSrc: str
    summary: str
    date: CarDate
    type: str
    transmission: str
    hp: str
    price: int
