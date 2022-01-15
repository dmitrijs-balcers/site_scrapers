import re
from typing import Tuple, Dict, Optional

from gazpacho import Soup
from returns.pipeline import flow
from returns.result import safe

from site_scrapers.models.Car import CarDate, CarFull, Country, FuelType, BodyType, Drivetrain
from site_scrapers.scrapers.utils import parse_price, find_one, find_many

DOMAIN = "https://lietotiauto.mollerauto.lv"


@safe
def scrape_moller_car_detail(html: str) -> CarFull:
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
        lambda _: _.map(lambda v: v.attrs["content"]),
        lambda _: _.map(lambda _: re.sub(r"\/[^\/]+\/$", "", _))
    ).value_or("")

    return CarFull(
        url=url,
        summary=find_one("h1")(soup).map(lambda _: _.text).value_or(""),
        transmission=details.get('Pārnesumkārba:'),
        hp=details.get('Jauda:'),
        type=details.get('Virsbūves tips:'),
        body=parse_body(details.get('Virsbūves tips:')),
        date=parse_date(details.get('Pirmā reģistrācija:')),
        color=details.get('Krāsa:'),
        engineSize=parse_int(details.get('Dzinēja tilpums:')),
        mileage=parse_int(details.get('Nobraukums:')),
        fuelType=parse_fuel_type(details.get('Degviela:')),
        hasWarranty=parse_warranty(details.get('Garantija:')),
        doors=details.get('Durvju skaits:'),
        vin=details.get('Virsbūves (VIN) numurs:'),
        registrationNo=details.get('Reģistrācijas numurs:'),
        techInspDate=parse_date(details.get('Tehniskā skate:')),
        drivetrain=parse_drivetrain(details.get('Piedziņa:')),
        price=parse_price(info['Cena:']),
        dealer="moller-auto",
        country=parse_country(info.get('Valsts:')),
        previewImgSrc="https://lietotiauto.mollerauto.lv" + imageSrc
    )


def parse_country(country: Optional[str]) -> Optional[Country]:
    if country == "Latvija":
        return "lv"
    if country == "Lietuva":
        return "lt"
    if country == "Igaunija":
        return "ee"
    return None


def parse_date(date: Optional[str]) -> Optional[CarDate]:
    if date is None:
        return None

    d = date.split("/")
    return CarDate(d[0], d[1])


def parse_int(mileage: Optional[str]) -> Optional[int]:
    if mileage is None:
        return None

    return int(re.findall(r'\d+', mileage.replace(" ", ""))[0])


def parse_fuel_type(fuelType: Optional[str]) -> Optional[FuelType]:
    if fuelType == "benzīns":
        return "petrol"
    if fuelType == "dīzelis":
        return "diesel"
    return None


def parse_body(body: Optional[str]) -> Optional[BodyType]:
    if body == "sedans":
        return "sedan"
    if body == "universāls":
        return "wagon"
    if body == "pikaps":
        return "pickup"
    return None


def parse_warranty(warranty: Optional[str]) -> Optional[bool]:
    if warranty == "Ražotāja garantija":
        return True
    return None


def parse_drivetrain(drivetrain: Optional[str]) -> Optional[Drivetrain]:
    if drivetrain == "pilnpiedziņa":
        return "awd"
    if drivetrain == "priekšējā piedziņa":
        return "fwd"
    if drivetrain == "aizmugures piedziņa":
        return "rwd"
    return None
