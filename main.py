import asyncio
import time
from itertools import chain
from typing import List, Iterable, Sequence

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
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def fetch_cars(car: Iterable[Car]) -> Sequence[FutureResultE[str]]:
    futures: Sequence[FutureResultE[str]] = await asyncio.gather(
        *[fetch_car_html(car.url) for car in car]
    )

    return futures

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

    car_details = asyncio.run(fetch_cars(res))
    print(car_details)

    print(*res, sep="\n")
    print("--- %s seconds ---" % (time.time() - start_time))
