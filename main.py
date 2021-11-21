import asyncio
import time
from itertools import chain, islice, takewhile, repeat
from typing import List, Iterable, Sequence, TypeVar, Tuple

import httpx
from returns.future import future_safe, FutureResultE
from returns.iterables import Fold
from returns.result import Result, Success

from models.Car import Car
from scrapers.brcAuto import fetch_brc_auto_list
from scrapers.mollerAuto import fetch_moller_auto_list
from scrapers.inchcape import fetch_inchcape_list

import multiprocessing as mp


@future_safe
async def fetch_car_html(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


T = TypeVar('T')


def split_every(n: int, iterable: Iterable[T]) -> Iterable[Iterable[T]]:
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


async def fetch_cars(urls: Iterable[str]) -> List[FutureResultE[str]]:
    futures: List[FutureResultE[str]] = await asyncio.gather(
        *[fetch_car_html(u) for u in urls]
    )

    return futures


async def aaa(res: Iterable[Car]) -> List[FutureResultE[str]]:
    url_batches = split_every(10, [car.url for car in res])
    car_details: List[FutureResultE[str]] = []
    for url_batch in url_batches:
        car_details = car_details + await fetch_cars(url_batch)

    return car_details


if __name__ == "__main__":
    start_time = time.time()
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())

    results: List[Result[Iterable[Car], str]] = []

    [
        pool.apply_async(fn, callback=lambda r: results.append(r))
        for fn in [fetch_moller_auto_list, fetch_inchcape_list, fetch_brc_auto_list]
    ]

    pool.close()
    pool.join()

    res: Iterable[Car] = chain(*Fold.collect(results, Success.from_value(())).value_or(()))


    car_details = asyncio.run(aaa(res))
    print(car_details)

    print(*res, sep="\n")
    print("--- %s seconds ---" % (time.time() - start_time))
