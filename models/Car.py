from dataclasses import dataclass
from typing import NamedTuple, Literal

CarDate = NamedTuple("CarDate", [("month", str), ("year", str)])


@dataclass
class Car:
    url: str
    previewImgSrc: str
    summary: str
    date: CarDate
    type: str
    # TODO: put literal here with automatic/manual
    transmission: str
    hp: str
    price: int

@dataclass
class CarFull(Car):
    vin: str
    registrationNo: str
    mileage: int
    engineSize: int
    techInspDate: CarDate
    fuelType: Literal["petrol", "diesel"]
    body: Literal["sedan", "hatchback", "wagon", "pickup", "suv"]
    drivetrain: Literal["front", "awd", "back"]
