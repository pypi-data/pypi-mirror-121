import asyncio
from typing import Callable, TypeVar

from tortfunc.exceptions import FunctionTimeOut

T = TypeVar("T")


def asyncio_timeout(function: Callable[[T, T], T], timeout: float) -> Callable[[T, T], T]:
    async def wrapper(*args, **kwargs):
        try:
            res = await asyncio.wait_for(function(*args, **kwargs), timeout=timeout)
        except asyncio.TimeoutError:
            raise FunctionTimeOut

        return res

    return wrapper
