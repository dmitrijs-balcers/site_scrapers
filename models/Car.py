from dataclasses import dataclass
from typing import NamedTuple, Literal, Optional

CarDate = NamedTuple("CarDate", [("month", str), ("year", str)])
Drivetrain = Optional[Literal["front", "awd", "back"]]
BodyType = Literal["sedan", "hatchback", "wagon", "pickup", "suv"]
FuelType = Literal["petrol", "diesel"]
Country = Literal["lv", "lt", "ee"]
Dealer = Literal["moller"]



@dataclass
class Car:
    url: str
    previewImgSrc: str
    summary: str
    # first registration date
    date: CarDate
    type: str
    # TODO: put literal here with automatic/manual
    transmission: str
    # TODO: put int here
    hp: str
    price: int


@dataclass
class CarFull(Car):
    vin: str
    registrationNo: str
    mileage: int
    engineSize: int
    techInspDate: CarDate
    fuelType: Optional[FuelType]
    body: Optional[BodyType]
    drivetrain: Drivetrain
    color: str
    hasWarranty: Optional[bool]
    doors: str
    country: Optional[Country]
    dealer: Dealer
