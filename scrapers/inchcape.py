import re
from typing import Iterable

from gazpacho import Soup
from returns.pipeline import flow
from returns.result import Result, Success, Failure
from scrapers.utils import find_one, find_many, parse_price

from models.Car import Car, CarDate


def parse_inchcape(page: int = 1) -> Result[Iterable[Car], str]:
    soup = Soup.get(
        url=f"https://certified.inchcape.lv/auto-ajax?drive=AWD&catalog_page={page}&_=1637248077760",
    )

    cars = soup.find("div", {"class": "offer js-offer"})

    if type(cars) is not list:
        return Failure("failed to acquire cars")

    def parse_car(car: Soup) -> Car:
        url = flow(
            car,
            find_one("a"),
            lambda anchor: anchor.map(lambda _: _.attrs),
            lambda _: _.bind(lambda attrs: attrs["href"]),
        )

        imageSrc = flow(
            car,
            find_one("div", {"class": "offer__image-wrap js-offer-image active"}),
            lambda _: _.bind(find_one("img")),
            lambda _: _.bind(lambda i: i.attrs["src"]),
            lambda src: src.replace("64x48", "640x480")
        )

        summary: str = flow(
            car,
            find_one("a", {"class": "offer__title"}),
            lambda anchor: anchor.bind(lambda _: _.text)
        )

        details = flow(
            car,
            find_many("div", {"class": "offer__feature-value"}),
            lambda d: d.bind(lambda _: [detail.text for detail in _])
        )

        date = details[0].split("-")
        hp = re.findall("[0-9]+\skW|[0-9]+\shp", summary)[0]

        price: str = flow(
            car,
            find_one("div", {"class": "offer__price"}),
            lambda op: op.bind(find_one("span", {"class": "new"})),
            lambda _: _.bind(lambda p: p.text)
        )

        return Car(
            summary=summary,
            date=CarDate(date[1], date[0]),
            price=parse_price(price),
            hp=hp,
            transmission=details[5],
            type=details[1],
            previewImgSrc="https://certified.inchcape.lv" + imageSrc,
            url="https://certified.inchcape.lv" + url,
        )

    return Success([parse_car(car) for car in cars])
