from typing import Iterable

from gazpacho import Soup
from returns.pipeline import flow
from site_scrapers.scrapers.utils import find_one, find_many


def fetch_brc_auto_urls(page: int = 1) -> Iterable[str]:
    print("fetch_brc_auto_urls")
    soup = Soup.get(
        url=f"https://lv.brcauto.eu/lietoti-auto?city=5&search=1&driving_wheelbase=3&page={page}",
    )

    return flow(
        soup,
        find_many("div", {"class": "cars"}),
        lambda _: _.bind(lambda _: _),
        lambda _: [flow(
            car,
            find_one("h2", {"class": "cars__title"}),
            lambda _: _.bind(find_one("a")),
            lambda _: _.bind(lambda _: _.attrs["href"]),
        ) for car in _],
    )
