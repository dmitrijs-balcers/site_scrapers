from typing import Union, List, Iterable

import requests
from gazpacho import Soup
from returns.maybe import Maybe
from returns.methods import unwrap_or_failure
from returns.pipeline import is_successful, flow
from returns.result import Result, Failure, Success

from models.Car import Car, CarDate

DOMAIN = "https://lietotiauto.mollerauto.lv"


def parse_moller_auto() -> Result[Iterable[Car], str]:
    r = requests.post(
        url=f"{DOMAIN}/lv/usedcars/search",
        data={"ajaxsearch": 1, "search_drivetrain": 10003016},
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
    summary = car.find("div", {"class": "vehiclesummary"}).find("a")  # type: ignore
    data = car.find("div", {"class": "vehicledata"})

    if (type(data) is not list) or (type(summary) is not Soup):
        return Failure("failed to parse vehicle data")

    normalized_details = normalize_details(data[0])

    if type(normalized_details) is not Soup:
        return Failure("failed to normalize details")

    details: list[str] = normalized_details.text.split(", ")
    date = details[0].split("/")

    return Success(Car(
        summary=summary.text,
        date=CarDate(date[0], date[1]),
        price=get_price(data[1]),
        hp=details[2],
        transmission=details[3],
        type=details[4],
        url=f"{DOMAIN}{get_url(summary)}",
    ))


def normalize_details(html: Soup) -> Union[List[Soup], Soup, None]:
    return Soup(html.__str__().replace("<br>", ", ")).find("div")


def get_price(html: Soup) -> str:
    price = html.find("span")

    if type(price) is Soup and price:
        return price.text

    return html.text


def get_url(summary: Soup) -> str:
    return Maybe.from_optional(summary.attrs).map(lambda v: v["href"]).value_or("")
