from typing import Iterable

from gazpacho import Soup
from returns.pipeline import flow
from scrapers.utils import find_one, parse_price
from returns.pointfree import bind
from returns.result import Result, Success, Failure

from models.Car import Car, CarDate, CarFull


# def fetch_brc_auto_list(page: int = 1) -> CarFull:
