from typing import NamedTuple, TypedDict

CarDate = NamedTuple("CarDate", [("month", str), ("year", str)])


class Car(TypedDict):
    summary: str
    date: CarDate
    type: str
    transmission: str
    hp: str
    price: str
