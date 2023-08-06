from functools import partial
from typing import Callable, TypeVar

import backoff

from .exceptions import FunctionTimeOut
from .registry import Registry
from .timeout import timeout_registry

T = TypeVar("T")

retry_dict = {
    "expo": backoff.expo,
    "constant": backoff.constant,
    "fibo": backoff.fibo,
    "none": None,
}

retry_registry = Registry(name="retry", reg=retry_dict)


def create_timeout(timeout_method="thread", timeout_kwargs={}):
    timeout_func = timeout_registry[timeout_method]
    return partial(timeout_func, **timeout_kwargs)


def create_retry(wait_gen="expo", backoff_kwargs={}):
    if isinstance(wait_gen, str):
        wait_gen = retry_registry[wait_gen]
    return backoff.on_exception(wait_gen, FunctionTimeOut, **backoff_kwargs)


def create_timeout_retry(
    func: Callable[[T, T], T],
    timeout_method="thread",
    timeout_kwargs={},
    wait_gen="expo",
    backoff_kwargs={},
):
    timeout_func = create_timeout(timeout_method=timeout_method, timeout_kwargs=timeout_kwargs)
    retry_func = create_retry(
        wait_gen=wait_gen,
        backoff_kwargs=backoff_kwargs,
    )
    return retry_func(timeout_func(func))


def timeout_retry(
    timeout_method="thread",
    timeout_kwargs={},
    wait_gen="expo",
    backoff_kwargs={},
):
    def tort_decorator(func: Callable[[T, T], T]):
        return create_timeout_retry(
            func,
            timeout_method=timeout_method,
            timeout_kwargs=timeout_kwargs,
            wait_gen=wait_gen,
            backoff_kwargs=backoff_kwargs,
        )

    return tort_decorator
