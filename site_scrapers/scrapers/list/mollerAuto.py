from typing import Iterable

import requests
from gazpacho import Soup
from returns.maybe import Maybe
from returns.pipeline import flow

from site_scrapers.scrapers.utils import find_one, find_many

DOMAIN = "https://lietotiauto.mollerauto.lv"


def fetch_moller_urls(page: int = 1) -> Iterable[str]:
    print("fetch_moller_urls")
    r = requests.post(
        url=f"{DOMAIN}/lv/usedcars/search",
        data={"ajaxsearch": 1, "search_drivetrain": 10003016, "page": page},
    )
    soup = Soup(r.text.encode().decode("unicode-escape").replace("\/", "/"))

    return flow(
        soup,
        find_many("div", {"class": "vehicle"}),
        lambda _: _.bind(lambda _: _),
        lambda _: [flow(
            car,
            find_one("div", {"class": "vehiclesummary"}),
            lambda _: _.bind(find_one("a")),
            lambda _: _.bind(lambda _: f"{DOMAIN}{get_url(_)}"),
        ) for car in _],
    )


def get_url(summary: Soup) -> str:
    return Maybe.from_optional(summary.attrs).map(lambda v: v["href"]).value_or("")
