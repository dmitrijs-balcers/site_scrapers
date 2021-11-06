from typing import Union, List

import requests
from gazpacho import Soup
from returns.result import Result, Failure, Success

from models.Car import Car, CarDate


def parse_moller_auto() -> None:
    r = requests.post(
        url="https://lietotiauto.mollerauto.lv/lv/usedcars/search",
        data={"ajaxsearch": 1, "search_drivetrain": 10003016},
    )

    carsHtml = r.text.encode().decode("unicode-escape").replace("\/", "/")

    soup = Soup(carsHtml)

    cars = soup.find("div", {"class": "vehicle"})

    if type(cars) is not list:
        return

    print(*[parse(car) for car in cars], sep="\n")


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
        type=details[4]
    ))


def normalize_details(html: Soup) -> Union[List[Soup], Soup, None]:
    return Soup(html.__str__().replace("<br>", ", ")).find("div")


def get_price(html: Soup) -> str:
    price = html.find("span")

    if type(price) is Soup and price:
        return price.text
    
    return html.text
