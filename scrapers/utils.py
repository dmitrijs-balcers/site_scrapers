from typing import Optional, Dict, Any, Callable, List

from gazpacho import Soup
from returns.maybe import Maybe, Some, Nothing
import re


def find_one(tag: str, attrs: Optional[Dict[str, Any]] = None) -> Callable[[Soup], Maybe[Soup]]:
    def _(soup: Soup) -> Maybe[Soup]:
        result = soup.find(tag, attrs, partial=False)

        if type(result) is Soup:
            return Some(result)

        if type(result) is list:
            return Some(result[0])

        return Nothing

    return _


def find_many(tag: str, attrs: Optional[Dict[str, Any]] = None) -> Callable[[Soup], Maybe[List[Soup]]]:
    def _(soup: Soup) -> Maybe[List[Soup]]:
        result = soup.find(tag, attrs, partial=False, mode='all')

        if type(result) is Soup:
            return Some([result])

        if type(result) is list:
            return Some(result)

        return Nothing

    return _


def parse_price(price: str) -> int:
    return int(re.findall(r'\d+', price.replace(" ", ""))[0])
