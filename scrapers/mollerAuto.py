import re
from typing import Union, List, Iterable

import requests
from gazpacho import Soup
from returns.maybe import Maybe
from returns.methods import unwrap_or_failure
from returns.pipeline import is_successful, flow
from returns.result import Result, Failure, Success

from models.Car import Car, CarDate
from scrapers.utils import parse_price, find_one, find_many

DOMAIN = "https://lietotiauto.mollerauto.lv"


def parse_moller_auto(page: int = 1) -> Result[Iterable[Car], str]:
    r = requests.post(
        url=f"{DOMAIN}/lv/usedcars/search",
        data={"ajaxsearch": 1, "search_drivetrain": 10003016, "page": page},
    )

    carsHtml = r.text.encode().decode("unicode-escape").replace("\/", "/")

    soup = Soup(carsHtml)

    cars = soup.find("div", {"class": "vehicle"})

    if type(cars) is not list:
        return Failure("issue parsing vehicles")

    return Success(flow(
        [parse(car) for car in cars],
        lambda _: filter(is_successful, _),
        lambda _: [unwrap_or_failure(car) for car in _],
    ))


def parse(car: Soup) -> Result[Car, str]:
    imageSrc = flow(
        car,
        find_one("div", {"class": "image"}),
        lambda _: _.bind(lambda i: find_one("a")(i)),
        lambda _: _.bind(lambda a: a.attrs["style"]),
        lambda style: re.findall("\/lv.*jpg", style)[0],
        lambda imgSrc: re.sub("\/h=\d.*\/", "/w=374/", imgSrc)
    )
    summary = flow(
        find_one("div", {"class": "vehiclesummary"})(car),
        lambda _: _.bind(lambda c: find_one("a")(c)),
        lambda _: _.bind(lambda c: c),

    )

    data: List[Soup] = (find_many("div", {"class": "vehicledata"})(car)).value_or([])

    normalized_details = normalize_details(data[0])

    if type(normalized_details) is not Soup:
        return Failure("failed to normalize details")

    details: list[str] = normalized_details.text.split(", ")
    date = details[0].split("/")

    return Success(Car(
        summary=summary.text,
        date=CarDate(date[0], date[1]),
        price=parse_price(data[1].text),
        hp=details[2],
        transmission=details[3],
        type=details[4],
        url=f"{DOMAIN}{get_url(summary)}",
        previewImgSrc=f"{DOMAIN}{imageSrc}"
    ))


def normalize_details(html: Soup) -> Union[List[Soup], Soup, None]:
    return Soup(html.__str__().replace("<br>", ", ")).find("div")


def get_url(summary: Soup) -> str:
    return Maybe.from_optional(summary.attrs).map(lambda v: v["href"]).value_or("")
