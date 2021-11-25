from gazpacho import Soup
from returns.pipeline import flow
from returns.result import Result, Success, Failure
from scrapers.utils import find_one, find_many, parse_price

from models.Car import Car, CarDate, CarFull


# def fetch_inchcape_list(page: int = 1) -> CarFull:
#     return CarFull()
