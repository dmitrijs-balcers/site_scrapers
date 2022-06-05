from typing import Iterable

from gazpacho import Soup
from returns.pipeline import flow
from returns.pointfree import bind

from site_scrapers.scrapers.utils import find_one, find_many


def fetch_inchcape_urls(page: int = 1) -> Iterable[str]:
    print("fetch_inchcape_urls")
    soup = Soup.get(
        url=f"https://certified.inchcape.lv/auto-ajax?&catalog_page={page}",
    )

    return flow(
        soup,
        find_many("article", {"class": "products__item js-product-item"}),
        lambda _: _.map(lambda _: [flow(
            car,
            find_one("a"),
            lambda _: _.map(lambda _: f"https://certified.inchcape.lv/{_.attrs['href']}"),
            lambda _: _.bind(lambda _: _)
        ) for car in _]),
        lambda _: _.bind(lambda _: _)
    )
