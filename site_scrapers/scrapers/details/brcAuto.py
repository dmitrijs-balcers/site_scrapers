from typing import Tuple, Optional
import re
from gazpacho import Soup
from returns.pipeline import flow
from returns.result import safe

from site_scrapers.scrapers.utils import find_one, find_many, parse_price

from site_scrapers.models.Car import CarDate, CarFull, Drivetrain, BodyType, FuelType


@safe
def scrape_brc_auto_car_detail(html: str) -> CarFull:
    soup = Soup(html)
    summary = flow(
        soup,
        find_one("h1", {"class": "font-bold text-2xl lg:text-3xl mb-1"}),
        lambda _: _.bind(lambda _: _.text)
    )

    url = flow(
        soup,
        find_one("ul", {"class": "header__langs"}),
        lambda _: _.bind(find_one("li")),
        lambda _: _.bind(find_one("a")),
        lambda _: _.bind(lambda _: _.attrs["href"])
    )

    previewImgSrc = flow(
        soup,
        find_one("a", {"class": "swiper-slide"}),
        lambda _: _.bind(lambda _: _.attrs["data-thumb"])
    )

    def get_spec(spec: Soup) -> Tuple[str, str]:
        name: str = flow(find_one("use")(spec), lambda _: _.bind(lambda _: _.attrs["xlink:href"]))
        value: str = flow(find_one("span")(spec), lambda _: _.bind(lambda _: _.text))
        return name, value

    data = flow(
        soup,
        find_one("ul", {"class": "car-specs"}),
        lambda _: _.bind(find_many("li")),
        lambda _: _.bind(lambda _: [get_spec(spec) for spec in _]),
        dict
    )

    vin = flow(
        soup,
        find_one("div", {"class": "car-section__content"}),
        lambda _: _.bind(find_one("p")),
        lambda _: _.bind(find_one("a")),
        lambda _: _.bind(lambda _: _.attrs["href"]),
        lambda _: _.split("=")[1]
    )

    price = flow(
        soup,
        find_one("div", {"class": "mt-1 cars-price font-black lg:text-2xl leading-none"}),
        lambda _: _.bind(lambda _: _.text)
    )

    return CarFull(
        url=url,
        previewImgSrc=previewImgSrc,
        summary=summary,
        date=CarDate(month='00', year=data["#calendar"].replace(" g.", "")),
        type=data.get("#body"),
        transmission=data.get("#gearbox"),
        hp=data.get("#power"),
        price=parse_price(price),
        vin=vin,
        registrationNo=None,
        mileage=parse_int(data.get("#speedometer")),
        engineSize=None,
        techInspDate=None,
        fuelType=parse_fuel_type(data.get("#fuel")),
        body=parse_body(data.get("#body")),
        drivetrain=parse_drivetrain(data.get("#wheels")),
        color=None,
        hasWarranty=True if "Garantija" in list(data.values()) else False,
        doors=data.get("#doors"),
        country='lv',
        dealer='brc-auto'
    )


def parse_int(mileage: Optional[str]) -> Optional[int]:
    if mileage is None:
        return None

    return int(re.findall(r'\d+', mileage.replace(" ", ""))[0])


def parse_fuel_type(fuelType: Optional[str]) -> Optional[FuelType]:
    if fuelType is None:
        return None

    if "Benzīns" in fuelType:
        return "petrol"
    if "Dīzelis" in fuelType:
        return "diesel"
    if fuelType == "Plug-in Hibrīds":
        return "hybrid"
    return None


def parse_body(body: Optional[str]) -> Optional[BodyType]:
    if body == "Sedans":
        return "sedan"
    if body == "Universālis":
        return "wagon"
    if body == "Pikaps":
        return "pickup"
    if body == "Apvidus":
        return "suv"
    if body == "Hečbeks":
        return "hatchback"
    if body == "Minivans":
        return "minivan"
    if body == "MOTO":
        return "motorcycle"
    if body == "Kupeja":
        return "coupe"
    return None


def parse_drivetrain(drivetrain: Optional[str]) -> Optional[Drivetrain]:
    if drivetrain == "Pilnpiedziņas":
        return "awd"
    if drivetrain == "Priekšējais":
        return "fwd"
    if drivetrain == "Aizmugurējais":
        return "rwd"
    return None
