import asyncio
import time
from itertools import islice, takewhile, repeat, chain
from typing import List, Iterable, Sequence, TypeVar, Callable

import httpx
from returns.functions import tap
from returns.pipeline import flow
from returns.converters import flatten
from returns.future import future_safe, FutureResultE
from returns.io import IOResultE
from returns.iterables import Fold
from returns.pointfree import map_, bind

from models.Car import Car, CarFull
from scrapers.details.brcAuto import scrape_brc_auto_car_detail
from scrapers.details.inchcape import scrape_inchcape_car_detail
from scrapers.details.mollerAuto import scrape_moller_car_detail
from scrapers.list.brcAuto import fetch_brc_auto_list
from scrapers.list.mollerAuto import fetch_moller_auto_list
from scrapers.list.inchcape import fetch_inchcape_list

from utils.sync_to_async import sync_to_async


@future_safe
async def fetch_car_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


CarHtmlFutures = Iterable[FutureResultE[str]]
CarFullFutures = Iterable[FutureResultE[CarFull]]
T = TypeVar('T')
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')


def split_every(n: int, iterable: Iterable[T]) -> Iterable[Iterable[T]]:
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


@future_safe
async def fetch_car_htmls(urls: Iterable[str]) -> CarHtmlFutures:
    return iter(await asyncio.gather(
        *[fetch_car_html(u) for u in urls]
    ))


def flatten_iter(v: Iterable[Iterable[T]]) -> Iterable[T]:
    return chain(*v)


def fetch_cars_in_batches(res: Iterable[Car]) -> FutureResultE[CarHtmlFutures]:
    url_batches = split_every(10, [car.url for car in res])
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


def fetch_car_pages(
        get_cars: Callable[..., FutureResultE[Iterable[Car]]],
        car_parser: Callable[[str], CarFull]
) -> FutureResultE[CarFullFutures]:
    future_cars: FutureResultE[Iterable[Car]] = get_cars()

    car_htmls: FutureResultE[CarHtmlFutures] = flow(
        future_cars,
        map_(fetch_cars_in_batches),
        flatten
    )

    return flow(
        car_htmls,
        lambda _: _.map(lambda _: [flow(
            car,
            lambda _: _.bind(lambda _: _),
            car_parser,
        ) for car in _]),
    )


async def gather_lists() -> Sequence[IOResultE[List[FutureResultE[str]]]]:
    car_futures = [
        fetch_car_pages(sync_to_async(fn[0]), fn[1])
        for fn in [
            (fetch_moller_auto_list, scrape_moller_car_detail),
            (fetch_inchcape_list, scrape_inchcape_car_detail),
            (fetch_brc_auto_list, scrape_brc_auto_car_detail),
        ]
    ]

    rs = await asyncio.gather(*car_futures)

    return rs


if __name__ == "__main__":
    start_time = time.time()
    # Sequence of lists with html strings
    results: Sequence[IOResultE[List[FutureResultE[str]]]] = asyncio.run(gather_lists())

    # r2 = [flow(
    #     result,
    #     lambda _: _.bind(lambda _: _),
    #     lambda _: [flow(res, lambda _: _.bind(lambda _: _)) for res in _],
    #     lambda _: [scrape_brc_auto_car_detail(el) for el in _]
    # ) for result in results]

    # [print(*rr, sep="\n") for rr in r2]
    # print(*r2, sep="\n")
    print(*results, sep="\n")

    # result = asyncio.run(fetch_car_html("https://lv.brcauto.eu/automobilis/c832466-bmw-220-2.0l-mehaniska").awaitable())
    # print(flow(result, bind(scrape_brc_auto_car_detail)))

    print("--- %s seconds ---" % (time.time() - start_time))
