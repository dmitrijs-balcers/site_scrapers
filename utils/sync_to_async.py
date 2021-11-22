import asyncio
import functools
from typing import TypeVar, Tuple, Dict, Callable, Awaitable

from mypy_extensions import VarArg, KwArg

T = TypeVar('T')
T1 = TypeVar('T1')
R = TypeVar('R')


def sync_to_async(fn: Callable[..., R]) -> Callable[[VarArg(Tuple[T, ...]), KwArg(Dict[str, T1])], Awaitable[R]]:
    @functools.wraps(fn)
    async def wrapper(*args: Tuple[T, ...], **kwargs: Dict[str, T1]) -> R:
        loop = asyncio.get_event_loop()
        p_func = functools.partial(fn, *args, **kwargs)
        return await loop.run_in_executor(None, p_func)

    return wrapper
