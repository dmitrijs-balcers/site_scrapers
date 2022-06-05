# !!!IMPORTANT!!!
#
# Use no JS Mode to get HTML!!!!
import re
from typing import Tuple, Optional

from gazpacho import Soup
from returns.pipeline import flow
from returns.result import safe

from site_scrapers.scrapers.utils import find_one, find_many

from site_scrapers.models.Car import CarDate, CarFull, FuelType, BodyType, Drivetrain


@safe
def scrape_inchcape_car_detail(html: str) -> CarFull:
    soup = Soup(html)

    url = flow(
        soup,
        find_one("input", {"type": "hidden", "name": "url"}),
        lambda _: _.bind(lambda _: _.attrs["value"]),
    )

    previewImg = flow(
        soup,
        find_one("a", {"class": "gallery__item"}, True),
        lambda _: _.bind(lambda _: _.attrs["href"]),
    )

    summary = flow(
        find_one("h1", {"class": "title"})(soup),
        lambda _: _.bind(lambda _: _.text)
    )

    def get_feature(feature: Soup) -> Tuple[str, str]:
        name: str = flow(find_one("span", {"class": "car-props__list-key"}, True)(feature),
                         lambda _: _.bind(lambda _: _.text))
        value: str = flow(find_one("div", {"class": "car-props__list-val"}, True)(feature),
                          lambda _: _.bind(lambda _: _.text))

        return name, value

    features = flow(
        find_many("div", {"class": "car-props__list-right"})(soup),
        lambda _: _.map(lambda fs: [get_feature(feature) for feature in fs]),
        lambda _: _.bind(dict)
    )

    date = features["Izlaiduma gads"].split("-")

    price = flow(
        soup,
        find_one("div", {"class": "car-props__cost"}, True),
        lambda _: _.map(lambda _: _.text),
        lambda _: _.bind(parse_int)
    )

    def get_info(feature: Soup) -> Tuple[str, str]:
        name: str = flow(find_one("div", {"class": "insert-tab__tech-key"})(feature),
                         lambda _: _.bind(lambda _: _.text))
        value: str = flow(find_one("div", {"class": "insert-tab__tech-val"})(feature),
                          lambda _: _.bind(lambda _: _.text))

        return name, value

    info = flow(
        find_many("li", {"class": "insert-tab__tech-row"}, True)(soup),
        lambda _: _.map(lambda _: [get_info(information) for information in _]),
        lambda _: _.bind(lambda _: dict(_))
    )

    return CarFull(
        url=url,
        previewImgSrc="https://certified.inchcape.lv" + previewImg,
        summary=summary,
        date=CarDate("00", date[0]),
        type=features.get("Virsbūves tips"),
        transmission=features.get("Pārnesumkārba"),
        hp=re.findall("[0-9]+\s?kW|[0-9]+\shp", summary, flags=re.IGNORECASE)[0],
        price=price or -1,
        vin=info.get("VIN"),
        registrationNo=None,
        mileage=parse_int(features.get("Nobraukums")),
        engineSize=parse_int(features.get("Dzinēja tilpums")),
        techInspDate=None,
        fuelType=parse_fuel_type(features.get("Dzinējs")),
        body=parse_body(features.get("Virsbūves tips")),
        drivetrain=parse_drivetrain(features.get("Piedziņas veids")),
        color=None,
        # Claims to have on every car for 6 months
        hasWarranty=True,
        doors=None,
        country="lv",
        dealer="inchcape",
    )


def parse_int(mileage: Optional[str]) -> Optional[int]:
    if mileage is None:
        return None

    return int(re.findall(r'\d+', mileage.replace(" ", ""))[0])


def parse_fuel_type(fuelType: Optional[str]) -> Optional[FuelType]:
    if fuelType == "Benzīns":
        return "petrol"
    if fuelType == "Dīzeļdegviela":
        return "diesel"
    if fuelType == "Hibrīds":
        return "hybrid"
    return None


def parse_body(body: Optional[str]) -> Optional[BodyType]:
    if body == "Sedans":
        return "sedan"
    if body == "Universālis":
        return "wagon"
    if body == "Pikaps":
        return "pickup"
    if body == "SUV":
        return "suv"
    if body == "Hečbeks":
        return "hatchback"
    if body == "Minivans":
        return "minivan"
    if body == "MOTO":
        return "motorcycle"
    return None


def parse_drivetrain(drivetrain: Optional[str]) -> Optional[Drivetrain]:
    if drivetrain == "AWD":
        return "awd"
    if drivetrain == "FWD":
        return "fwd"
    if drivetrain == "RWD":
        return "rwd"
    return None
