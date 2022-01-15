import asyncio
from itertools import islice, takewhile, repeat, chain
from typing import Iterable, Sequence, TypeVar, Callable, Tuple

import httpx
from returns.pipeline import flow
from returns.converters import flatten
from returns.future import future_safe, FutureResultE
from returns.io import IOResultE
from returns.iterables import Fold
from returns.pointfree import map_
from returns.result import ResultE, Success

from site_scrapers.models.Car import CarFull
from site_scrapers.scrapers.details.brcAuto import scrape_brc_auto_car_detail
from site_scrapers.scrapers.details.inchcape import scrape_inchcape_car_detail
from site_scrapers.scrapers.details.mollerAuto import scrape_moller_car_detail
from site_scrapers.scrapers.list.brcAuto import fetch_brc_auto_urls
from site_scrapers.scrapers.list.mollerAuto import fetch_moller_urls
from site_scrapers.scrapers.list.inchcape import fetch_inchcape_urls

from site_scrapers.utils.sync_to_async import sync_to_async

ListScraper = Callable[[int], Iterable[str]]
CarHtmlFutures = Iterable[FutureResultE[str]]

CarScraperResult = ResultE[CarFull]
CarScraper = Callable[[str], CarScraperResult]
CarFullFutures = Iterable[FutureResultE[CarScraperResult]]

T = TypeVar('T')
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')


async def scrape_all() -> Iterable[CarFull]:
    return await scrape_specific([
        (fetch_moller_urls, scrape_moller_car_detail),
        (fetch_inchcape_urls, scrape_inchcape_car_detail),
        (fetch_brc_auto_urls, scrape_brc_auto_car_detail),
    ])


# Will return successfully parsed instances
async def scrape_specific(scrapers: Iterable[Tuple[ListScraper, CarScraper]]) -> Iterable[CarFull]:
    car_futures: Sequence[FutureResultE[CarFullFutures]] = [
        fetch_car_pages(sync_to_async(list_scraper), car_scraper)
        for (list_scraper, car_scraper) in scrapers
    ]

    cars: Sequence[IOResultE[Tuple[CarFullFutures, ...]]] = await asyncio.gather(*car_futures)

    res = flow(
        Fold.collect(cars, IOResultE.from_value(())),
        lambda _: _.bind(lambda _: _),
        lambda _: flatten_iter(_),
    )

    return flow(
        Fold.collect_all(res, IOResultE.from_value(())),
        lambda _: _.bind(lambda _: Fold.collect_all(_, Success(()))),
        lambda _: _.bind(lambda _: _)
    )


def fetch_car_pages(
        get_urls: Callable[..., FutureResultE[Iterable[str]]],
        car_parser: CarScraper
) -> FutureResultE[CarFullFutures]:
    future_cars: FutureResultE[Iterable[str]] = get_urls()

    car_htmls: FutureResultE[CarHtmlFutures] = flow(
        future_cars,
        map_(fetch_cars_in_batches),
        flatten
    )

    return flow(
        car_htmls,
        lambda _: _.map(lambda _: [car.map(car_parser) for car in _]),
    )


def fetch_cars_in_batches(res: Iterable[str]) -> FutureResultE[CarHtmlFutures]:
    url_batches = split_every(10, res)
    futures_of_batched_car_details_futures = tuple([fetch_car_htmls(url_batch) for url_batch in url_batches])

    future_of_batched_car_details_futures = flow(
        futures_of_batched_car_details_futures,
        lambda _: Fold.collect(_, FutureResultE.from_value(()))
    )

    future_of_car_details_futures: FutureResultE[CarHtmlFutures] = flow(
        future_of_batched_car_details_futures,
        map_(flatten_iter)
    )

    return future_of_car_details_futures


@future_safe
async def fetch_car_htmls(urls: Iterable[str]) -> CarHtmlFutures:
    return iter(await asyncio.gather(
        *[fetch_car_html(u) for u in urls]
    ))


@future_safe
async def fetch_car_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def split_every(n: int, iterable: Iterable[T]) -> Iterable[Iterable[T]]:
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


def flatten_iter(v: Iterable[Iterable[T]]) -> Iterable[T]:
    return chain(*v)
