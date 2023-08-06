from tortfunc.registry import Registry

from .async_timeout import asyncio_timeout
from .thread_timeout import threaded_timeout

timeout_registry = Registry(
    name="timeout",
    default_method="thread",
    reg={"thread": threaded_timeout, "async": asyncio_timeout},
)
