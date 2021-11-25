import re
from typing import Tuple, Dict, Optional

from gazpacho import Soup
from returns.pipeline import flow
from returns.pointfree import bind

from models.Car import CarDate, CarFull, Country, FuelType, BodyType
from scrapers.utils import parse_price, find_one, find_many

DOMAIN = "https://lietotiauto.mollerauto.lv"


def scrape_car_detail(html: str) -> CarFull:
    soup = Soup(html)

    def get_row_tuple(row: Soup) -> Tuple[str, str]:
        def extract_text(s: Soup) -> str:
            return s.text

        name: str = flow(find_one("th")(row), lambda _: _.bind(extract_text))
        value: str = flow(find_one("td")(row), lambda _: _.bind(extract_text))
        return name, value

    def get_table_dict(which_table: int) -> Dict[str, str]:
        return flow(
            soup,
            find_many("table"),
            lambda _: _.bind(lambda v: v[which_table]),
            find_many("tr"),
            lambda _: _.bind(lambda rows: tuple(get_row_tuple(row) for row in rows)),
            dict
        )

    info = get_table_dict(0)
    details = get_table_dict(1)
    imageSrc = flow(find_one("a", {"class": "fancybox"})(soup), lambda _: _.bind(lambda v: v.attrs["href"]))
    url = flow(
        find_one("meta", {"property": "og:url"})(soup),
        lambda _: _.map(lambda v: v.attrs["content"])
    ).value_or("")

    return CarFull(
        url=url,
        summary=find_one("h1")(soup).map(lambda _: _.text).value_or(""),
        transmission=details['Pārnesumkārba:'],
        hp=details['Jauda:'],
        type=details['Virsbūves tips:'],
        body=parse_body(details['Virsbūves tips:']),
        date=parse_date(details['Pirmā reģistrācija:']),
        color=details['Krāsa:'],
        engineSize=parse_int(details['Dzinēja tilpums:']),
        mileage=parse_int(details['Nobraukums:']),
        fuelType=parse_fuel_type(details['Degviela:']),
        hasWarranty=parse_warranty(details['Garantija:']),
        doors=details['Durvju skaits:'],
        vin=details['Virsbūves (VIN) numurs:'],
        registrationNo=details['Reģistrācijas numurs:'],
        techInspDate=parse_date(details['Tehniskā skate:']),
        drivetrain=None,
        price=parse_price(info['Cena:']),
        dealer="moller",
        country=parse_country(info['Valsts:']),
        previewImgSrc="https://lietotiauto.mollerauto.lv" + imageSrc
    )


def parse_country(country: str) -> Optional[Country]:
    if country == "Latvija":
        return "lv"
    if country == "Lietuva":
        return "lt"
    return None


def parse_date(date: str) -> CarDate:
    d = date.split("/")
    return CarDate(d[0], d[1])


def parse_int(mileage: str) -> int:
    return int(re.findall(r'\d+', mileage.replace(" ", ""))[0])


def parse_fuel_type(fuelType: str) -> Optional[FuelType]:
    if fuelType == "benzīns":
        return "petrol"
    if fuelType == "dīzelis":
        return "diesel"
    return None


def parse_body(body: str) -> Optional[BodyType]:
    if body == "sedans":
        return "sedan"
    if body == "universāls":
        return "wagon"
    return None


def parse_warranty(warranty: str) -> Optional[bool]:
    if warranty == "Ražotāja garantija":
        return True
    return None
