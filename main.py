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

from models.Car import Car
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


def fetch_car_pages(get_cars: Callable[..., FutureResultE[Iterable[Car]]]) -> FutureResultE[CarHtmlFutures]:
    future_cars: FutureResultE[Iterable[Car]] = get_cars()

    return flow(
        future_cars,
        map_(fetch_cars_in_batches),
        flatten
    )


async def gather_lists() -> Sequence[IOResultE[List[FutureResultE[str]]]]:
    return await asyncio.gather(*[
        fetch_car_pages(sync_to_async(fn))
        for fn in [
            # fetch_moller_auto_list,
            # fetch_inchcape_list,
            # fetch_brc_auto_list,
        ]
    ])


if __name__ == "__main__":
    start_time = time.time()
    # Sequence of lists with html strings
    # results: Sequence[IOResultE[List[FutureResultE[str]]]] = asyncio.run(gather_lists())

    # r2 = [flow(
    #     result,
    #     lambda _: _.bind(lambda _: _),
    #     lambda _: [flow(res, lambda _: _.bind(lambda _: _)) for res in _],
    #     lambda _: [scrape_brc_auto_car_detail(el) for el in _]
    # ) for result in results]

    # [print(*rr, sep="\n") for rr in r2]
    # print(*r2, sep="\n")

    # result = asyncio.run(fetch_car_html("https://lv.brcauto.eu/automobilis/c832466-bmw-220-2.0l-mehaniska").awaitable())
    # print(flow(result, bind(scrape_brc_auto_car_detail)))

    print("--- %s seconds ---" % (time.time() - start_time))
