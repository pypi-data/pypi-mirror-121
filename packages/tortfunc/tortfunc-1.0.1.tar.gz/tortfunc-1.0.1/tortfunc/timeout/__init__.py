from tortfunc.registry import Registry

from .thread_timeout import threaded_timeout

timeout_registry = Registry(
    name="timeout", default_method="thread", reg={"thread": threaded_timeout}
)
