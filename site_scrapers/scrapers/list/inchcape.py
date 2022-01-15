from typing import Iterable

from gazpacho import Soup
from returns.pipeline import flow
from site_scrapers.scrapers.utils import find_one, find_many


def fetch_inchcape_urls(page: int = 1) -> Iterable[str]:
    print("fetch_inchcape_urls")
    soup = Soup.get(
        url=f"https://certified.inchcape.lv/auto-ajax?drive=AWD&catalog_page={page}&_=1637248077760",
    )

    return flow(
        soup,
        find_many("div", {"class": "offer__info-row"}),
        lambda _: _.bind(lambda _: _),
        lambda _: [flow(
            car,
            find_one("a"),
            lambda anchor: anchor.map(lambda _: _.attrs),
            lambda _: _.bind(lambda attrs: attrs["href"]),
            lambda _: f"https://certified.inchcape.lv/{_}"
        ) for car in _],
    )
