import asyncio
import time
from itertools import islice, takewhile, repeat
from typing import List, Iterable, Sequence, TypeVar, Tuple, Callable, Coroutine, Awaitable

import httpx
from returns._internal.pipeline.flow import flow
from returns.converters import flatten
from returns.future import future_safe, FutureResultE
from returns.io import IOResultE, IO
from returns.iterables import Fold
from returns.pointfree import bind, map_

from models.Car import Car
from scrapers.brcAuto import fetch_brc_auto_list
from scrapers.mollerAuto import fetch_moller_auto_list
from scrapers.inchcape import fetch_inchcape_list

import multiprocessing as mp

from utils.sync_to_async import sync_to_async


@future_safe
async def fetch_car_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


CarHtmlFutures = Tuple[FutureResultE[str], ...]
T = TypeVar('T')
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')


def split_every(n: int, iterable: Iterable[T]) -> Iterable[Iterable[T]]:
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


@future_safe
async def fetch_car_htmls(urls: Iterable[str]) -> CarHtmlFutures:
    return tuple(await asyncio.gather(
        *[fetch_car_html(u) for u in urls]
    ))


def flatten_tuples(v: Tuple[Tuple[T, ...], ...]) -> Tuple[T, ...]:
    return tuple(sum(v, ()))


def fetch_cars_in_batches(res: Iterable[Car]) -> FutureResultE[CarHtmlFutures]:
    url_batches = split_every(10, [car.url for car in res])
    futures_of_batched_car_details_futures = tuple([fetch_car_htmls(url_batch) for url_batch in url_batches])

    future_of_batched_car_details_futures = flow(
        futures_of_batched_car_details_futures,
        lambda _: Fold.collect(_, FutureResultE.from_value(()))
    )

    future_of_car_details_futures: FutureResultE[CarHtmlFutures] = flow(
        future_of_batched_car_details_futures,
        map_(flatten_tuples)
    )

    return future_of_car_details_futures


def fetch_car_pages(get_cars: Callable[..., FutureResultE[Iterable[Car]]]) -> FutureResultE[
    Tuple[FutureResultE[str], ...]]:
    future_cars: FutureResultE[Iterable[Car]] = get_cars()

    return flow(
        future_cars,
        map_(fetch_cars_in_batches),
        flatten
    )


async def gather_lists() -> Sequence[IOResultE[List[FutureResultE[str]]]]:
    return await asyncio.gather(*[
        fetch_car_pages(sync_to_async(fn))
        for fn in [fetch_moller_auto_list, fetch_inchcape_list, fetch_brc_auto_list]
    ])


if __name__ == "__main__":
    start_time = time.time()
    # Sequence of lists with html strings
    results: Sequence[IOResultE[List[FutureResultE[str]]]] = asyncio.run(gather_lists())

    print(*results, sep="\n")
    print("--- %s seconds ---" % (time.time() - start_time))
