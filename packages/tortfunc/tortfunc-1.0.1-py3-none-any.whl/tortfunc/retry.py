from typing import Callable, TypeVar

import backoff

from .exceptions import FunctionTimeOut
from .timeout import timeout_registry
from .types import RegistryManifest

T = TypeVar("T")


def timeout_retry(
    timeout_manifest: RegistryManifest, max_tries: int = None, max_time: float = None
):
    def tort_decorator(func: Callable[[T, T], T]):
        return create_timeout_retry(
            func, timeout_manifest=timeout_manifest, max_tries=max_tries, max_time=max_time
        )

    return tort_decorator


def create_timeout_retry(
    func: Callable[[T, T], T],
    timeout_manifest: RegistryManifest,
    max_tries: int = None,
    max_time: float = None,
):
    timeout_key = timeout_manifest.get("method")
    timeout_method = timeout_registry[timeout_key]
    timeout_spec = timeout_manifest.get("spec", {})
    timed_out_func = timeout_method(func, **timeout_spec)
    dec = backoff.on_exception(
        backoff.expo, FunctionTimeOut, max_tries=max_tries, max_time=max_time
    )
    return dec(timed_out_func)


def retry_function(
    func: Callable[[T, T], T], timeout_manifest: RegistryManifest
) -> Callable[[T, T], T]:
    timeout_key = timeout_manifest.get("method")
    timeout_method = timeout_registry[timeout_key]
    timeout_spec = timeout_manifest.get("spec", {})
    timed_out_func = timeout_method(func, **timeout_spec)

    def retry_timedout(*args, **kwargs):
        try:
            return timed_out_func(*args, **kwargs)
        except TimeoutError:
            return timed_out_func(*args, **kwargs)

    return retry_timedout
