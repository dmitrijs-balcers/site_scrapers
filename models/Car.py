from dataclasses import dataclass
from typing import NamedTuple, Literal, Optional

CarDate = NamedTuple("CarDate", [("month", str), ("year", str)])
Drivetrain = Literal["fwd", "awd", "rwd"]
BodyType = Literal["sedan", "hatchback", "wagon", "pickup", "suv", "minivan", "motorcycle", "coupe"]
FuelType = Literal["petrol", "diesel", "hybrid"]
Country = Literal["lv", "lt", "ee"]
Dealer = Literal["moller-auto", "inchcape", "brc-auto"]


@dataclass
class CarFull():
    url: str
    previewImgSrc: str
    summary: str
    # first registration date
    date: Optional[CarDate]
    type: Optional[str]
    # TODO: put literal here with automatic/manual
    transmission: Optional[str]
    # TODO: put int here
    hp: Optional[str]
    price: int
    vin: Optional[str]
    registrationNo: Optional[str]
    mileage: Optional[int]
    engineSize: Optional[int]
    techInspDate: Optional[CarDate]
    fuelType: Optional[FuelType]
    body: Optional[BodyType]
    drivetrain: Optional[Drivetrain]
    color: Optional[str]
    hasWarranty: Optional[bool]
    doors: Optional[str]
    country: Optional[Country]
    dealer: Dealer
